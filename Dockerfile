# Build stage with uv
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

# Add metadata
LABEL maintainer="Nobel Khandaker" \
      version="0.1.0" \
      description="Random Number Server using MCP"

# Set working directory
WORKDIR /app

# Enable bytecode compilation for better performance
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since we're building for deployment
ENV UV_LINK_MODE=copy

# Install system dependencies if needed
RUN apk add --no-cache gcc musl-dev

# Copy dependency files first for better caching
COPY pyproject.toml README.md ./

# Generate lockfile and install dependencies
RUN uv lock && \
    uv sync --frozen --no-install-project --no-dev

# Copy source code
COPY src/ ./src/

# Install the project itself
RUN uv sync --frozen --no-dev

# Remove unnecessary files to reduce size
RUN find /app/.venv -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true && \
    find /app/.venv -type f -name '*.pyc' -delete && \
    find /app/.venv -type f -name '*.pyo' -delete && \
    find /app/.venv -type d -name 'tests' -exec rm -rf {} + 2>/dev/null || true && \
    find /app/.venv -type d -name 'test' -exec rm -rf {} + 2>/dev/null || true && \
    rm -rf /app/.venv/lib/python*/site-packages/*.dist-info/RECORD && \
    rm -rf /app/.venv/lib/python*/site-packages/*.dist-info/INSTALLER

# Final stage - minimal runtime image
FROM python:3.13-alpine

# Install runtime dependencies
RUN apk add --no-cache libgcc

# Create non-root user for security
RUN adduser -D -h /home/app -s /bin/sh app

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Copy source code from builder
COPY --from=builder --chown=app:app /app/src /app/src
COPY --from=builder --chown=app:app /app/pyproject.toml /app/pyproject.toml
COPY --from=builder --chown=app:app /app/uv.lock /app/uv.lock

# Install uv in the final image for running the application
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Switch to non-root user
USER app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1
ENV UV_PYTHON="/app/.venv/bin/python"
ENV LOG_LEVEL=INFO

# Note: Health check removed as MCP servers run continuously through stdio
# and standard health checks would interfere with the server's operation

# Use uv to run the server
ENTRYPOINT ["uv", "run", "--frozen", "src/random_server.py"]

# Alternative: Direct Python execution (uncomment if preferred)
# ENTRYPOINT ["/app/.venv/bin/python", "-m", "src.random_server"]