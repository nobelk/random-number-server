# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based MCP (Model Context Protocol) server that generates random numbers using weather data as seeds. The server uses FastMCP framework and exposes a tool for generating random numbers based on weather API data.

## Architecture

- **src/RandomNumberGenerator.py**: Core random number generation logic using Linear Congruential Generator algorithm with weather data as seeds
- **src/random_server.py**: FastMCP server implementation that exposes the random number generation as an MCP tool
- **tests/**: Comprehensive unit tests with 86% code coverage

## Development Commands

### Setup and Dependencies
```bash
# Install dependencies using uv
uv sync

# Build/install the project in editable mode
uv pip install -e .
```

### Running the Server

#### Option 1: Using Docker Compose (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the server
docker-compose down
```

#### Option 2: Using uv directly
```bash
# Run the MCP server (from project root)
uv run src/random_server.py

# Or with absolute path
uv --directory /Users/Nobel.Khandaker/sources/random-number-server run src/random_server.py
```

### Testing
```bash
# Run all tests locally
uv run pytest

# Run tests with coverage report
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_random_number_generator.py
uv run pytest tests/test_random_server.py

# Run tests with verbose output
uv run pytest -v

# Run tests in Docker container
docker-compose run --rm --entrypoint /app/.venv/bin/python random-server -m pytest
```

## Docker Configuration

### Files
- **Dockerfile**: Multi-stage build with Python 3.13 Alpine, optimized to ~110MB
- **docker-compose.yml**: Production configuration with resource limits and logging
- **docker-compose.dev.yml**: Development overrides with live code reloading
- **.env.example**: Environment variable template

### Docker Commands
```bash
# Build Docker image
docker build -t random-number-server:latest .

# Run with Docker Compose (production)
docker-compose up -d

# Run with Docker Compose (development)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Execute tests in container
docker-compose run --rm --entrypoint /app/.venv/bin/python random-server -m pytest
```

## Key Implementation Details

- The RandomNumberGenerator uses weather API data from open-meteo.com as seeds
- Linear Congruential Generator algorithm with constants: A=8191, C=524287, M=6700417
- Coordinates rotate after each weather data fetch to vary the seed source
- Server uses FastMCP for MCP protocol implementation with stdio transport
- Comprehensive error handling and logging throughout
- Docker container runs as non-root user 'app' for security
- Multi-stage Docker build reduces final image size by ~50%

## MCP Configuration

The server is configured to work with Claude Desktop. Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/absolute/path/to/random-number-server",
        "run",
        "src/random_server.py"
      ]
    }
  }
}
```