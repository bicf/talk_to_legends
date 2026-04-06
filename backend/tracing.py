"""Optional OpenTelemetry tracing — enabled via OTEL_ENABLED=true|log."""

import os

_initialized = False


def init_tracing():
    global _initialized
    if _initialized:
        return
    _initialized = True

    mode = os.getenv("OTEL_ENABLED", "").lower()
    # the `console` mode deliver in stdout the traces
    if mode not in ("true", "console"):
        return

    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.resources import Resource

    resource = Resource.create({"service.name": "talk-to-legends"})
    provider = TracerProvider(resource=resource)

    if mode == "true":
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

        otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")
        exporter = OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces")
        provider.add_span_processor(BatchSpanProcessor(exporter))
    else:  # mode == "console"
        from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(provider)

    # Instrument Django HTTP layer and requests
    try:
        from opentelemetry.instrumentation.django import DjangoInstrumentor
        DjangoInstrumentor().instrument()
    except ImportError:
        pass

    try:
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
        RequestsInstrumentor().instrument()
    except ImportError:
        pass
