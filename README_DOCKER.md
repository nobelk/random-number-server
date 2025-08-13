# Docker Setup for Random Number Server

This document provides instructions for running the Random Number Server using Docker and Docker Compose.

## Prerequisites

- Docker Engine (version 20.10 or later)
- Docker Compose (version 2.0 or later)

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and start the container:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Stop the container:**
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t random-number-server:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d --name random-server random-number-server:latest
   ```

3. **View logs:**
   ```bash
   docker logs -f random-server
   ```

4. **Stop and remove:**
   ```bash
   docker stop random-server && docker rm random-server
   ```

## Development Setup

For development with live code reloading:

```bash
# Use both compose files
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## Environment Variables

Copy `.env.example` to `.env` and adjust values:

- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `PYTHONUNBUFFERED` - Ensure output is displayed immediately

## Testing the Container

Test that the container is working:

```bash
# Run a test command
docker-compose run --rm --entrypoint /app/.venv/bin/python random-server -c \
  "import asyncio; from src.RandomNumberGenerator import RandomNumberGenerator; \
   g = RandomNumberGenerator(); print(f'Random: {asyncio.run(g.random())}')"
```

## Container Details

- **Base Image:** Python 3.13 Alpine (minimal size)
- **Final Size:** ~110MB
- **User:** Runs as non-root user 'app'
- **Working Directory:** `/app`
- **Entrypoint:** `uv run --frozen src/random_server.py`

## Resource Limits

The Docker Compose configuration includes resource limits:
- **CPU:** 1.0 cores max, 0.25 cores reserved
- **Memory:** 256MB max, 128MB reserved

## Volumes

- `mcp-logs` - Named volume for application logs (optional)

## Network

Uses default bridge network for container isolation.

## Troubleshooting

1. **Container won't start:**
   ```bash
   docker-compose logs --tail=50
   ```

2. **Permission issues:**
   Ensure files are readable by the 'app' user in the container.

3. **Module import errors:**
   Rebuild the image after code changes:
   ```bash
   docker-compose build --no-cache
   ```