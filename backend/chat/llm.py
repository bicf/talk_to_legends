import json
from django.conf import settings
from datapizza.clients.openai_like import OpenAILikeClient
from opentelemetry import trace

from chat.models import Session, Prompt


tracer = trace.get_tracer(__name__)


def build_prompt(session, context="") -> str:
    legend = session.legend
    lang = session.lang
    try:
        prompt_obj = Prompt.objects.get(lang=lang)
        system_prompt = prompt_obj.content.format(
            name=legend.name,
            lang=lang,
            description=legend.description,
            biography=legend.biography,
            context=context
        ).strip()
    except Prompt.DoesNotExist:
        system_prompt = (
            f"You are {legend.name}. Respond in character, in first person, "
            f"in language '{lang}', "
            f"drawing on what is publicly known about your life, work, and era. "
            f"{legend.description} {legend.biography}\n\n{context}"
        ).strip()
    return system_prompt


def ask(session: Session, user_message: str, llm_url: str, llm_model: str, llm_api_key: str) -> str:
    with tracer.start_as_current_span("llm_ask") as span:
        model = llm_model
        base_url = llm_url
        api_key = llm_api_key

        span.set_attribute("legend", session.legend.name)
        span.set_attribute("legend_slug", session.legend.slug)
        span.set_attribute("model", model)
        span.set_attribute("session_id", str(session.id))

        # Get last 4 messages for context
        messages = session.messages.order_by('-created_at')[:5]
        # Reverse to have them in chronological order
        messages = reversed(messages[1:])
        context_parts = []
        for i,msg in enumerate(messages):
            role = "You" if msg.role == "assistant" else "User"
            span.set_attribute(f"message_{i}", msg.content)
            context_parts.append(f"{role}: {msg.content}")
        
        context = "\n".join(context_parts)
        system_prompt = build_prompt(session, context=context)
        client = OpenAILikeClient(
            api_key=api_key,
            model=model,
            system_prompt=system_prompt,
            base_url=base_url,
        )
        response = client.invoke(user_message)
        content = getattr(response, 'content', response)

        span.set_attribute("system_prompt", system_prompt)
        span.set_attribute("user_message", user_message)

        if isinstance(content, list):
            span.set_attribute("response_type", "list")
            string_content = "\n".join([getattr(block, 'text', getattr(block, 'content', str(block))) for block in content])
            span.set_attribute("response", str(string_content))
            return string_content

        span.set_attribute("response", str(content))
        return str(content)