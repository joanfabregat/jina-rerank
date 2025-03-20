# Copyright (c) 2025 Joan Fabrégat <j@fabreg.at>
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, subject to the conditions in the full MIT License.
# The Software is provided "as is", without warranty of any kind.

ARG PYTHON_VERSION=3.13


# --- Builder Image ---
FROM python:${PYTHON_VERSION}-slim AS builder


WORKDIR /src

# Install uv and its dependencies
COPY --from=ghcr.io/astral-sh/uv:0.6.8 /uv /uvx /bin/
RUN chmod +x /bin/uv /bin/uvx && \
    uv venv .venv
ENV PATH="/src/.venv/bin:$PATH"

# Copy dependency specification and install production dependencies
COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-default-groups


# --- Final Image ---
FROM python:${PYTHON_VERSION}-slim AS final

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

WORKDIR /src

# Create a non-root user
RUN addgroup --system app && adduser --system --group --no-create-home app

# Copy the virtual environment
COPY --from=builder /src/.venv .venv
ENV PATH="/src/.venv/bin:$PATH"

# Copy the application code
COPY main.py /src/main.py

# Download the model
RUN mkdir -p /src/.model && python -m main download

# Use the non-root user
USER app:app

EXPOSE $PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1 --log-level info --timeout-keep-alive 0"]