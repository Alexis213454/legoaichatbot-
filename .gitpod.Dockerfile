# syntax=docker/dockerfile:1.4
FROM gitpod/workspace-full

USER root
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    curl \
 && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
 && update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install UV and make it available
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/gitpod/.cargo/bin:$PATH"

# Set UV to use copy mode to avoid hardlinking issues
ENV UV_LINK_MODE=copy

# Set working directory early
WORKDIR /workspace

# Copy ALL necessary files for the build (not just pyproject.toml)
COPY pyproject.toml ./
RUN echo "# LEGO RAG" > README.md
COPY uv.lock* ./

# Install dependencies only (no editable install yet)
RUN --mount=type=cache,target=/home/gitpod/.cache/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --no-editable

# Copy the rest of your code
COPY . .

# Set up persistent cache directories
RUN mkdir -p /workspace/.cache/pip /workspace/.cache/uv

# Set environment variables for caching
ENV PIP_CACHE_DIR=/workspace/.cache/pip
ENV UV_CACHE_DIR=/workspace/.cache/uv
ENV PYTHONPATH=/workspace

USER gitpod