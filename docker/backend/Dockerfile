FROM python:3.11-slim

RUN mkdir /build
WORKDIR /build

# Build process dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    git \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Expose runserver/gunicorn
EXPOSE 8000/tcp

# Full python requirements to support development
COPY ./requirements.txt /build/requirements.txt
RUN pip install -r /build/requirements.txt

# Run Django
WORKDIR /project
