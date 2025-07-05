# random-number-server
MCP server to generate random numbers using the national weather data as seeds.

## Unit Tests

The project includes comprehensive unit tests for both core modules with 85% code coverage.

### Running Tests

```bash
# Install dependencies
uv sync

# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run tests with coverage report
python -m pytest --cov=RandomNumberGenerator --cov=random_server --cov-report=term-missing

# Run specific test files
python -m pytest test_random_number_generator.py
python -m pytest test_random_server.py
```

### Test Coverage

- **RandomNumberGenerator.py**: 82% coverage (13 tests)
- **random_server.py**: 93% coverage (17 tests)
- **Total**: 85% coverage (30 tests)

Tests cover:
- Initialization and configuration
- Random number generation algorithms
- Weather API integration
- Error handling and edge cases
- FastMCP tool registration and execution
- Concurrent request handling

# Testing
## Run the MCP server

```bash
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/random-number-server run random_server.py
```

## Run claude desktop by customizing the following configuration
here `code ~/Library/Application\ Support/Claude/claude_desktop_config.json`

```JSON
{
  "mcpServers": {
    "weather": {
      "command": "/Users/Nobel.Khandaker/.pyenv/shims/uv",
      "args": [
        "--directory",
        "/Users/Nobel.Khandaker/sources/random-number-server",
        "run",
        "random_server.py"
      ]
    }
  }
}
```


