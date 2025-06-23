from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

from RandomNumberGenerator import RandomNumberGenerator

# Initialize FastMCP server
mcp = FastMCP("meteorandom")
generator = RandomNumberGenerator()

@mcp.tool()
async def get_random_number() -> str:
    """
    Get a Random Number between 0 and 1.

    """
    data = await generator.random()

    if not data:
        return "Unable to fetch random numbers."
    return str(data)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')