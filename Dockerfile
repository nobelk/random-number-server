# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python-3.10-alpine AS uv

# Install the project in '/app' dir
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since we have the mounted volume
ENV UV_LINK_MODE=copy

# Generate TOML lockfile first
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv lock

# Install the project dependencies
 RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Add rest of the project source code and install it
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-dev --no-editable

# Remove unnecessary files from the virtual environment before copying
RUN find /app/.venv -name '__pycache__' -type d -exec rm -fr {} + && \
    find /app/.venv -name '*.pyc' -delete && \
    find /app/.venv -name '*.pyo' -delete && \
    echo "Cleanup completed .venv"

# Final Stage
FROM python:3.10-alpine

# Create a non-root user
RUN adduser -D -h /home/app -s /bin/sh app
WORKDIR /app
USER app


# Copy the virtual environment from the previous stage
COPY --from=uv --chown=app:app /app/.venv /app/.venv

# Place executable scripts in PATH
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["uv", "--dir", "/app/random_server.py"]