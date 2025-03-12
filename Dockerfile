# Copyright (c) 2025 Joan Fabrégat <j@fabreg.at>
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, subject to the conditions in the full MIT License.
# The Software is provided "as is", without warranty of any kind.

ARG PYTHON_VERSION=3.13


# --- Builder Image ---
FROM python:${PYTHON_VERSION}-slim AS builder

ARG COMPUTE_DEVICE

WORKDIR /app

# Install uv and its dependencies
COPY --from=ghcr.io/astral-sh/uv:0.5.31 /uv /uvx /bin/
RUN chmod +x /bin/uv /bin/uvx && \
    uv venv .venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency specification and install production dependencies
COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-default-groups $( [ "$COMPUTE_DEVICE" = "gpu" ] && echo "--group gpu" )



# --- Final Image ---
FROM python:${PYTHON_VERSION}-slim AS final

ARG COMPUTE_DEVICE=cpu
ARG PORT=80
ARG VERSION
ARG BUILD_ID
ARG COMMIT_SHA

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=${PORT}
ENV VERSION=${VERSION}
ENV BUILD_ID=${BUILD_ID}
ENV COMMIT_SHA=${COMMIT_SHA}
ENV HF_HOME="/app/.cache/huggingface"
ENV COMPUTE_DEVICE=${COMPUTE_DEVICE}

WORKDIR /app

# Copy the virtual environment
COPY --from=builder /app/.venv .venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application code
COPY main.py .

# Ensure a non-root user
RUN addgroup --system app &&  \
    adduser --system --group --no-create-home app && \
    chmod -R +x .venv/bin/ && \
    chown -R app:app .
USER app

# Download the model
RUN python -m main download

EXPOSE $PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1 --log-level info --timeout-keep-alive 0"]