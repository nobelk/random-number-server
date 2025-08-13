from typing import Any
import httpx
import logging
from mcp.server.fastmcp import FastMCP

from src.RandomNumberGenerator import RandomNumberGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp: FastMCP = FastMCP("meteorandom")
generator: RandomNumberGenerator = RandomNumberGenerator()
logger.info("FastMCP server initialized")

@mcp.tool()
async def get_random_number() -> str:
    """
    Get a Random Number between 0 and 1.

    """
    try:
        data: float = await generator.random()
        logger.info(f"Generated random number: {data}")
        
        if not data:
            logger.warning("Generated random number is 0 or falsy")
            return "Unable to fetch random numbers."
        return str(data)
    except Exception as e:
        logger.error(f"Error generating random number: {e}")
        return "Unable to fetch random numbers."


if __name__ == "__main__":
    # Initialize and run the server
    logger.info("Starting FastMCP server with stdio transport")
    mcp.run(transport='stdio')