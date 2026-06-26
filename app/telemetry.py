import logging

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)

from opentelemetry._logs import set_logger_provider
from opentelemetry.instrumentation.logging import LoggingInstrumentor

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


tracer = trace.get_tracer("IntelliCart")


def setup_telemetry(app):

    resource = Resource.create(
        {
            "service.name": "IntelliCart"
        }
    )

    trace_provider = TracerProvider(resource=resource)

    trace_exporter = OTLPSpanExporter(
        endpoint="localhost:4317",
        insecure=True
    )

    trace_provider.add_span_processor(
        BatchSpanProcessor(trace_exporter)
    )

    trace.set_tracer_provider(trace_provider)

    logger_provider = LoggerProvider(
        resource=resource
    )

    log_exporter = OTLPLogExporter(
        endpoint="localhost:4317",
        insecure=True
    )

    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(log_exporter)
    )

    set_logger_provider(logger_provider)

    LoggingInstrumentor().instrument(
        set_logging_format=True
    )

    logging.basicConfig(
        level=logging.INFO
    )

    FastAPIInstrumentor.instrument_app(app)

    return trace.get_tracer("IntelliCart")