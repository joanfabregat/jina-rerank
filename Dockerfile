# Copyright (c) 2025 Joan Fabrégat <j@fabreg.at>
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, subject to the conditions in the full MIT License.
# The Software is provided "as is", without warranty of any kind.

ARG PYTHON_VERSION=3.13


# --- Builder Image ---
FROM python:${PYTHON_VERSION}-bookworm AS builder

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
FROM python:${PYTHON_VERSION}-bookworm AS final

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

# Install the CUDA toolkit if needed
# https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#network-repo-installation-for-debian
#RUN apt-get update
#RUN apt-get install -y wget
#RUN wget https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/cuda-keyring_1.1-1_all.deb
#RUN dpkg -i cuda-keyring_1.1-1_all.deb
#RUN apt-get update
#RUN apt-get -y install nvidia-cublas-cu126

#RUN if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
#        # If using the new DEB822 format
#        sed -i 's/Components: main/Components: main contrib non-free-firmware non-free/g' /etc/apt/sources.list.d/debian.sources; \
#    elif [ -f /etc/apt/sources.list ]; then \
#        # If using the traditional format in sources.list
#        sed -i '/^deb/ s/$/ contrib non-free-firmware non-free/' /etc/apt/sources.list; \
#    else \
#        # Fallback to creating our own sources file
#        echo "deb http://deb.debian.org/debian bookworm main contrib non-free-firmware non-free" > /etc/apt/sources.list; \
#    fi && \
#    apt-get update && \
#    apt-get upgrade -y && \
#    #apt-get install -y nvidia-cuda-toolkit && \
#    apt-get install -y libcublas12


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