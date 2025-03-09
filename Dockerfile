ARG PYTHON_VERSION=3.13

# --- Builder Stage ---
FROM python:${PYTHON_VERSION}-slim-bookworm AS builder
WORKDIR /app

# Install uv and its dependencies
COPY --from=ghcr.io/astral-sh/uv:0.5.31 /uv /uvx /bin/
RUN chmod +x /bin/uv /bin/uvx && \
    uv venv .venv --python ${PYTHON_VERSION}
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency specification and install production dependencies
COPY uv.lock pyproject.toml ./
RUN uv sync --frozen


# --- Final Image ---
FROM python:${PYTHON_VERSION}-slim-bookworm
WORKDIR /app

ARG PORT=80
ARG VERSION
ARG BUILD_ID
ARG COMMIT_SHA

ENV PORT=${PORT}
ENV VERSION=${VERSION}
ENV BUILD_ID=${BUILD_ID}
ENV COMMIT_SHA=${COMMIT_SHA}

# Copy only the needed virtual environment from builder
COPY --from=builder /app/.venv .venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy only necessary application files
COPY app/ ./app/

# Ensure a non-root user
RUN addgroup --system app &&  \
    adduser --system --group --no-create-home app && \
    chmod -R +x .venv/bin/ && \
    chown -R app:app .venv/
USER app

# https://cloud.google.com/run/docs/tips/python#optimize_gunicorn
# Expose the port the app runs on
EXPOSE $PORT

# Command to run the application
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}