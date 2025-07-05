"""Unit tests for random_server.py module."""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from mcp.server.fastmcp import FastMCP
from RandomNumberGenerator import RandomNumberGenerator


# Import the module under test
import random_server


class TestRandomServer:
    """Test suite for random_server module."""

    def test_mcp_initialization(self):
        """Test that FastMCP server is properly initialized."""
        assert isinstance(random_server.mcp, FastMCP)
        assert random_server.mcp.name == "meteorandom"

    def test_generator_initialization(self):
        """Test that RandomNumberGenerator is properly initialized."""
        assert isinstance(random_server.generator, RandomNumberGenerator)
        assert random_server.generator._coordinate == (42.5255, -71.7642)
        assert random_server.generator._seed == 0

    @pytest.mark.asyncio
    async def test_get_random_number_success(self):
        """Test successful random number generation."""
        # Mock the generator's random method
        with patch.object(random_server.generator, 'random') as mock_random:
            mock_random.return_value = 0.12345
            
            result = await random_server.get_random_number()
            
            mock_random.assert_called_once()
            assert result == "0.12345"

    @pytest.mark.asyncio
    async def test_get_random_number_zero_value(self):
        """Test handling of zero random value."""
        with patch.object(random_server.generator, 'random') as mock_random:
            mock_random.return_value = 0.0
            
            result = await random_server.get_random_number()
            
            mock_random.assert_called_once()
            # 0.0 is falsy in Python, so it triggers the error message
            assert result == "Unable to fetch random numbers."

    @pytest.mark.asyncio
    async def test_get_random_number_one_value(self):
        """Test handling of maximum random value."""
        with patch.object(random_server.generator, 'random') as mock_random:
            mock_random.return_value = 1.0
            
            result = await random_server.get_random_number()
            
            mock_random.assert_called_once()
            assert result == "1.0"

    @pytest.mark.asyncio
    async def test_get_random_number_none_value(self):
        """Test handling when generator returns None."""
        with patch.object(random_server.generator, 'random') as mock_random:
            mock_random.return_value = None
            
            result = await random_server.get_random_number()
            
            mock_random.assert_called_once()
            assert result == "Unable to fetch random numbers."

    @pytest.mark.asyncio
    async def test_get_random_number_false_value(self):
        """Test handling when generator returns False."""
        with patch.object(random_server.generator, 'random') as mock_random:
            mock_random.return_value = False
            
            result = await random_server.get_random_number()
            
            mock_random.assert_called_once()
            assert result == "Unable to fetch random numbers."

    @pytest.mark.asyncio
    async def test_get_random_number_empty_string(self):
        """Test handling when generator returns empty string."""
        with patch.object(random_server.generator, 'random') as mock_random:
            mock_random.return_value = ""
            
            result = await random_server.get_random_number()
            
            mock_random.assert_called_once()
            assert result == "Unable to fetch random numbers."

    @pytest.mark.asyncio
    async def test_get_random_number_exception_handling(self):
        """Test handling of exceptions from generator."""
        with patch.object(random_server.generator, 'random') as mock_random:
            mock_random.side_effect = Exception("Network error")
            
            with pytest.raises(Exception):
                await random_server.get_random_number()

    @pytest.mark.asyncio
    async def test_get_random_number_multiple_calls(self):
        """Test multiple calls to get_random_number."""
        mock_values = [0.123, 0.456, 0.789]
        
        with patch.object(random_server.generator, 'random') as mock_random:
            mock_random.side_effect = mock_values
            
            results = []
            for _ in range(3):
                result = await random_server.get_random_number()
                results.append(result)
            
            assert results == ["0.123", "0.456", "0.789"]
            assert mock_random.call_count == 3

    @pytest.mark.asyncio
    async def test_get_random_number_precision(self):
        """Test precision of random number conversion to string."""
        test_cases = [
            (0.123456789, "0.123456789"),
            (0.1, "0.1"),
            (0.0001, "0.0001"),
            (0.999999, "0.999999"),
        ]
        
        for test_value, expected in test_cases:
            with patch.object(random_server.generator, 'random') as mock_random:
                mock_random.return_value = test_value
                
                result = await random_server.get_random_number()
                assert result == expected

    @pytest.mark.asyncio
    async def test_tool_registration(self):
        """Test that the tool is properly registered with FastMCP."""
        # Check if the tool is registered
        tools = await random_server.mcp.list_tools()
        tool_names = [tool.name for tool in tools]
        assert "get_random_number" in tool_names

    @pytest.mark.asyncio
    async def test_tool_description(self):
        """Test the tool's description and metadata."""
        tools = await random_server.mcp.list_tools()
        get_random_tool = next(tool for tool in tools if tool.name == "get_random_number")
        
        assert get_random_tool.description.strip() == "Get a Random Number between 0 and 1."
        assert get_random_tool.inputSchema["type"] == "object"
        assert get_random_tool.inputSchema["properties"] == {}

    @pytest.mark.asyncio
    async def test_tool_execution_through_mcp(self):
        """Test tool execution through FastMCP."""
        with patch.object(random_server.generator, 'random') as mock_random:
            mock_random.return_value = 0.42
            
            # Execute the tool through FastMCP
            result = await random_server.mcp.call_tool("get_random_number", {})
            
            assert result[0].text == "0.42"
            mock_random.assert_called_once()

    @pytest.mark.asyncio
    async def test_concurrent_random_number_requests(self):
        """Test handling of concurrent requests."""
        async def mock_random_with_delay():
            await asyncio.sleep(0.01)  # Small delay to simulate async work
            return 0.5
        
        with patch.object(random_server.generator, 'random', side_effect=mock_random_with_delay):
            # Execute multiple concurrent requests
            tasks = [random_server.get_random_number() for _ in range(5)]
            results = await asyncio.gather(*tasks)
            
            # All results should be the same since we're mocking the same value
            assert all(result == "0.5" for result in results)
            assert len(results) == 5

    def test_module_constants(self):
        """Test module-level constants and imports."""
        assert hasattr(random_server, 'mcp')
        assert hasattr(random_server, 'generator')
        assert hasattr(random_server, 'get_random_number')
        
        # Check imports are properly handled
        assert random_server.RandomNumberGenerator is not None

    @pytest.mark.asyncio
    async def test_get_random_number_with_generator_state_change(self):
        """Test behavior when generator state changes between calls."""
        # First call returns a value
        with patch.object(random_server.generator, 'random') as mock_random:
            mock_random.return_value = 0.123
            result1 = await random_server.get_random_number()
            assert result1 == "0.123"
            
            # Second call returns None (simulating state change)
            mock_random.return_value = None
            result2 = await random_server.get_random_number()
            assert result2 == "Unable to fetch random numbers."