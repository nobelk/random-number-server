# random-number-server
MCP server to generate random numbers using the national weather data as seeds.


# Testing
## Run the MCP server

```bash
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/weather run weather.py
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


