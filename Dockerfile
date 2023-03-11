# syntax=docker/dockerfile:1.2
FROM python:3.10-slim-bullseye as base

# Add Labels for OCI Image Format Specification
LABEL org.opencontainers.image.vendor="Quartx"
LABEL org.opencontainers.image.authors="William Forde"
# LABEL org.opencontainers.image.title="Quartx Call Logger"
# LABEL org.opencontainers.image.description="CDR(Call Data Record) logger that sends call logs to the Quartx Call Monitoring service for analysis."
# LABEL org.opencontainers.image.url="https://quartx.ie"
# LABEL org.opencontainers.image.licenses="GPL-2.0-only"

# Build Arguments, used to pass in Environment Variables
ARG VERSION="latest"
ARG SENTRY_DSN=""
ARG REG_KEY=""

# Docker Environment Variables
ENV PYTHONUNBUFFERED=1
ENV DOCKERIZED=1
ENV ENVIRONMENT="Dockerized"
ENV DATA_LOCATION="/data"
ENV SENTRY_DSN=$SENTRY_DSN
ENV REG_KEY=$REG_KEY
ENV VIRTUAL_ENV=/opt/venv
ENV VERSION=$VERSION

# Image setup
RUN mkdir -p $DATA_LOCATION && \
    useradd -rm -d /home/runner -s /bin/bash -g users -G dialout -u 999 runner && \
    chown runner:users $DATA_LOCATION

# Copy required scripts
COPY data/99-serial.rules /etc/udev/rules.d/99-serial.rules
COPY data/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["calllogger"]


# Switch to full buster to be able to compile uptime & psutil
FROM python:3.10-bullseye as compiler

# Install the package in a virtual environment
COPY . /src
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir /src


# Switch back to base image to finish the build
FROM base

# Finalize build image
COPY --from=compiler $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
USER runner:users
