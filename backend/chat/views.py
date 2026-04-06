import uuid

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

from legends.models import Legend
from .models import Session, Message
from .serializers import (
    SessionSerializer,
    MessageSerializer,
    StartSessionSerializer,
    SendMessageSerializer,
)
from .llm import ask


class SessionDetailView(APIView):
    http_method_names = ['get']

    @extend_schema(
        operation_id="getSession",
        responses={200: SessionSerializer},
        description="Get session details and messages history."
    )
    def get(self, request, session_id):
        session = get_object_or_404(
            Session.objects.prefetch_related('messages'),
            pk=session_id
        )
        return Response(SessionSerializer(session).data)


class SessionStartView(APIView):
    """POST /api/chat/session/ — create (or no-op if exists) a session."""
    http_method_names = ['post']

    @extend_schema(
        request=StartSessionSerializer,
        responses={
            201: SessionSerializer,
            200: SessionSerializer,
        },
        description="Create (or no-op if exists) a chat session with a specific legend."
    )
    def post(self, request):
        session_id = uuid.uuid4()
        serializer = StartSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        legend = get_object_or_404(Legend, pk=serializer.validated_data['legend_id'])
        lang = serializer.validated_data.get('lang', legend.lang)
        session, created = Session.objects.get_or_create(
            pk=session_id, defaults={'legend': legend, 'lang': lang}
        )
        return Response(
            SessionSerializer(session).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class SessionMessageView(APIView):
    """POST /api/chat/session/<id>/message — send a message, return answer."""

    @extend_schema(
        operation_id="sendMessage",
        request=SendMessageSerializer,
        responses={
            201: OpenApiResponse(
                description="Message sent and assistant response received.",
                response={
                    'type': 'object',
                    'properties': {
                        'user': {'$ref': '#/components/schemas/Message'},
                        'assistant': {'$ref': '#/components/schemas/Message'},
                    }
                }
            ),
            502: OpenApiResponse(description="LLM error.")
        },
        description="Send a message to the legend and get a response."
    )
    def post(self, request, session_id):
        session = get_object_or_404(Session, pk=session_id)
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data['content']
        llm_url = serializer.validated_data.get('llm_url')
        llm_model = serializer.validated_data.get('llm_model')
        llm_api_key = serializer.validated_data.get('llm_api_key')

        if not llm_url or not llm_model or not llm_api_key:
            return Response(
                {'detail': 'LLM URL, Model and API Key are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_msg = Message.objects.create(
            session=session, role=Message.ROLE_USER, content=content
        )
        try:
            answer = ask(
                session,
                content,
                llm_url=llm_url,
                llm_model=llm_model,
                llm_api_key=llm_api_key
            )
        except Exception as exc:
            return Response(
                {'detail': f'LLM error: {exc}'},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        assistant_msg = Message.objects.create(
            session=session, role=Message.ROLE_ASSISTANT, content=answer
        )
        return Response(
            {
                'user': MessageSerializer(user_msg).data,
                'assistant': MessageSerializer(assistant_msg).data,
            },
            status=status.HTTP_201_CREATED,
        )