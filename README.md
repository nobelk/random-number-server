# random-number-server

[![CI](https://github.com/nobelk/random-number-server/actions/workflows/ci.yml/badge.svg)](https://github.com/nobelk/random-number-server/actions/workflows/ci.yml)
[![Docker](https://github.com/nobelk/random-number-server/actions/workflows/docker.yml/badge.svg)](https://github.com/nobelk/random-number-server/actions/workflows/docker.yml)
[![codecov](https://codecov.io/gh/nobelk/random-number-server/branch/main/graph/badge.svg?token=YOUR_TOKEN)](https://codecov.io/gh/nobelk/random-number-server)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

MCP server to generate random numbers using the national weather data as seeds.

## Build Instructions

### Local Development Build
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/nobelk/random-number-server.git
cd random-number-server

# Install dependencies and build the project
uv sync

# Install in editable mode for development
uv pip install -e .
```

### Docker Build
```bash
# Build the Docker image
docker build -t random-number-server:latest .

# Or use Docker Compose to build
docker-compose build
```

## Quick Start

### Using Docker Compose (Recommended)
```bash
# Build and run the server
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the server
docker-compose down
```

### Using uv directly
```bash
# Install dependencies
uv sync

# Run the server
uv run src/random_server.py
```

## Unit Tests

The project includes comprehensive unit tests for both core modules with 86% code coverage.

### Running Tests

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run tests with coverage report
uv run pytest --cov=src --cov-report=term-missing

# Run specific test files
uv run pytest tests/test_random_number_generator.py
uv run pytest tests/test_random_server.py
```

### Test Coverage

- **src/RandomNumberGenerator.py**: 83% coverage (13 tests)
- **src/random_server.py**: 92% coverage (17 tests)
- **Total**: 86% coverage (30 tests)

Tests cover:
- Initialization and configuration
- Random number generation algorithms
- Weather API integration
- Error handling and edge cases
- FastMCP tool registration and execution
- Concurrent request handling

## Docker Setup

The project includes Docker and Docker Compose configurations for easy deployment.

### Docker Image
- **Base:** Python 3.13 Alpine (optimized for size)
- **Size:** ~110MB
- **Security:** Runs as non-root user
- **Build:** Multi-stage build for optimization

### Docker Compose
```bash
# Production
docker-compose up -d

# Development (with live reload)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Run tests in container
docker-compose run --rm --entrypoint /app/.venv/bin/python random-server -m pytest
```

See [README_DOCKER.md](README_DOCKER.md) for detailed Docker instructions.

## MCP Configuration

### Run the MCP server locally

```bash
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/random-number-server run src/random_server.py
```

### Configure Claude Desktop
Edit `~/Library/Application\ Support/Claude/claude_desktop_config.json`

```JSON
{
  "mcpServers": {
    "weather": {
      "command": "/Users/Nobel.Khandaker/.pyenv/shims/uv",
      "args": [
        "--directory",
        "/Users/Nobel.Khandaker/sources/random-number-server",
        "run",
        "src/random_server.py"
      ]
    }
  }
}
```


