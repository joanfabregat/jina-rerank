ARG PYTHON_VERSION=3.13

# --- UV Builder Stage ---
FROM python:${PYTHON_VERSION}-slim AS builder

WORKDIR /app

ARG COMPUTE_DEVICE=cpu

COPY --from=ghcr.io/astral-sh/uv:0.5.31 /uv /uvx /bin/

RUN chmod +x /bin/uv /bin/uvx && \
    uv venv .venv --python ${PYTHON_VERSION}
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml .
COPY uv.lock .

RUN if [ "$COMPUTE_DEVICE" = "gpu" ]; then \
      uv sync --group gpu --frozen; \
    else \
      uv sync --frozen; \
    fi


# --- Final Image ---
FROM python:${PYTHON_VERSION}-slim AS final
WORKDIR /app

ARG PORT=80
ARG VERSION
ARG BUILD_ID
ARG COMMIT_SHA
ARG COMPUTE_DEVICE=cpu

ENV PORT=${PORT}
ENV VERSION=${VERSION}
ENV BUILD_ID=${BUILD_ID}
ENV COMMIT_SHA=${COMMIT_SHA}
ENV HF_HOME="/app/.cache/huggingface"
ENV COMPUTE_DEVICE=${COMPUTE_DEVICE}

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