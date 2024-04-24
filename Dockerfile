FROM python:3.9-slim

ARG BUILD_DATE
ARG BUILD_VERSION
ARG VCS_REF

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

LABEL org.label-schema.schema-version="1.0" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.name="syneder/ecs-anywhere-network-agent" \
    org.label-schema.description="Detects containers running without the connected network and connects them to the network specified in the label." \
    org.label-schema.vcs-url="https://github.com/syneder/ecs-anywhere-network-agent" \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.version=$BUILD_VERSION

COPY ./main.py /app/main.py
CMD ["python", "main.py"]
