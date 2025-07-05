# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python-3.10-alpine AS uv

# Add metadata
LABEL maintainer="Nobel Khandaker" \
      version="0.1.0" \
      description="Random Number Server using MCP"

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

# Copy application source code
COPY --chown=root:root *.py /app/
COPY --chown=root:root pyproject.toml /app/
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

# Update package manager for security
RUN apk update && apk upgrade

# Create a non-root user
RUN adduser -D -h /home/app -s /bin/sh app
WORKDIR /app

# Copy the virtual environment and application code from the previous stage
COPY --from=uv --chown=app:app /app/.venv /app/.venv
COPY --from=uv --chown=app:app /app/*.py /app/
COPY --from=uv --chown=app:app /app/pyproject.toml /app/

# Switch to non-root user
USER app

# Place executable scripts in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Expose port (if needed for future HTTP endpoints)
EXPOSE 8000

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import random_server; print('Server module loaded successfully')" || exit 1

# Use proper entrypoint
ENTRYPOINT ["python", "/app/random_server.py"]