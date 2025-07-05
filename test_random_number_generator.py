"""Unit tests for RandomNumberGenerator class."""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
import requests
from RandomNumberGenerator import RandomNumberGenerator


class TestRandomNumberGenerator:
    """Test suite for RandomNumberGenerator class."""

    def test_init_default_coordinate(self):
        """Test initialization with default coordinate."""
        generator = RandomNumberGenerator()
        assert generator._coordinate == (42.5255, -71.7642)
        assert generator._seed == 0

    def test_init_custom_coordinate(self):
        """Test initialization with custom coordinate."""
        custom_coord = (40.7128, -74.0060)
        generator = RandomNumberGenerator(coordinate=custom_coord)
        assert generator._coordinate == custom_coord
        assert generator._seed == 0

    def test_get_forecast_url(self):
        """Test forecast URL generation."""
        generator = RandomNumberGenerator()
        coordinate = (42.5255, -71.7642)
        url = generator._get_forecast_url(coordinate)
        expected_url = "https://api.open-meteo.com/v1/forecast?latitude=42.5255&longitude=120&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation&wind_speed_unit=ms&temperature_unit=fahrenheit"
        assert url == expected_url

    @pytest.mark.asyncio
    async def test_get_random_seed_success(self):
        """Test successful random seed generation."""
        generator = RandomNumberGenerator()
        mock_response = Mock()
        mock_response.content = json.dumps({
            "current": {
                "temperature_2m": 25.5
            }
        })
        
        with patch('requests.get', return_value=mock_response):
            await generator._get_random_seed()
            
        assert generator._seed == 25.5
        # Check coordinate rotation
        expected_lat = (42.5255 + 10) % 180
        expected_long = (-71.7642 + 10) % 180
        assert generator._coordinate == (expected_lat, expected_long)

    @pytest.mark.asyncio
    async def test_get_random_seed_http_error(self):
        """Test random seed generation with HTTP error."""
        generator = RandomNumberGenerator()
        mock_response = Mock()
        mock_http_error = requests.exceptions.HTTPError("API Error")
        mock_http_error.response = Mock()
        mock_http_error.response.text = "Error message"
        mock_response.raise_for_status.side_effect = mock_http_error
        
        with patch('requests.get', return_value=mock_response):
            with patch('builtins.print') as mock_print:
                await generator._get_random_seed()
                mock_print.assert_called_once_with("Error message")

    @pytest.mark.asyncio
    async def test_random_first_call(self):
        """Test random number generation on first call."""
        generator = RandomNumberGenerator()
        
        # Mock the seed generation to set seed value
        async def mock_get_seed():
            generator._seed = 100
        
        with patch.object(generator, '_get_random_seed', side_effect=mock_get_seed) as mock_get_seed:
            result = await generator.random()
            
            mock_get_seed.assert_called_once()
            # Verify LCG calculation
            expected_seed = (8191 * 100 + 524287) % 6700417
            expected_result = expected_seed / 6700417
            assert result == expected_result

    @pytest.mark.asyncio
    async def test_random_subsequent_calls(self):
        """Test random number generation on subsequent calls."""
        generator = RandomNumberGenerator()
        generator._seed = 100  # Set initial seed
        
        result1 = await generator.random()
        result2 = await generator.random()
        
        # Results should be different
        assert result1 != result2
        
        # Verify results are in range [0, 1]
        assert 0 <= result1 <= 1
        assert 0 <= result2 <= 1

    @pytest.mark.asyncio
    async def test_random_deterministic_sequence(self):
        """Test that random generation is deterministic for same seed."""
        generator1 = RandomNumberGenerator()
        generator2 = RandomNumberGenerator()
        
        # Set same seed
        generator1._seed = 12345
        generator2._seed = 12345
        
        result1 = await generator1.random()
        result2 = await generator2.random()
        
        assert result1 == result2

    @pytest.mark.asyncio
    async def test_random_boundary_values(self):
        """Test random generation with boundary seed values."""
        generator = RandomNumberGenerator()
        
        # Test with minimum seed
        generator._seed = 1
        result_min = await generator.random()
        assert 0 <= result_min <= 1
        
        # Test with maximum seed
        generator._seed = 6700416  # CONST_M - 1
        result_max = await generator.random()
        assert 0 <= result_max <= 1

    def test_constants(self):
        """Test that constants are properly defined."""
        assert RandomNumberGenerator.CONST_A == 8191
        assert RandomNumberGenerator.CONST_C == 524287
        assert RandomNumberGenerator.CONST_M == 6700417
        assert RandomNumberGenerator.CONST_MIN_VAL == 0
        assert RandomNumberGenerator.CONST_MAX_VAL == 6700417
        assert RandomNumberGenerator.CONST_CITY_COORDINATE == (42.5255, -71.7642)

    @pytest.mark.asyncio
    async def test_coordinate_rotation_multiple_calls(self):
        """Test coordinate rotation over multiple seed generations."""
        generator = RandomNumberGenerator()
        original_coord = generator._coordinate
        
        # Mock successful API calls
        mock_response = Mock()
        mock_response.content = json.dumps({
            "current": {
                "temperature_2m": 20.0
            }
        })
        
        with patch('requests.get', return_value=mock_response):
            # First call
            await generator._get_random_seed()
            first_coord = generator._coordinate
            
            # Second call
            await generator._get_random_seed()
            second_coord = generator._coordinate
            
        # Coordinates should be different after each call
        assert original_coord != first_coord
        assert first_coord != second_coord

    @pytest.mark.asyncio
    async def test_json_parsing_error(self):
        """Test handling of JSON parsing errors."""
        generator = RandomNumberGenerator()
        mock_response = Mock()
        mock_response.content = b"invalid json"
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(json.JSONDecodeError):
                await generator._get_random_seed()

    @pytest.mark.asyncio
    async def test_network_timeout(self):
        """Test handling of network timeout."""
        generator = RandomNumberGenerator()
        
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout("Timeout error")
            
            with pytest.raises(requests.exceptions.Timeout):
                await generator._get_random_seed()