"""Random number generator class.
It is used for generating random numbers based on hourly weather forecasting data.
"""

import json
import logging
from typing import Optional, Tuple
import requests


class RandomNumberGenerator:
    CONST_CITY_COORDINATE = (42.5255, -71.7642)
    
    def __init__(self, coordinate: Optional[Tuple[float, float]] = None) -> None:
        self.logger = logging.getLogger(__name__)
        if coordinate:
            self._coordinate = coordinate
        else:
            self._coordinate = self.CONST_CITY_COORDINATE
        self._seed = 0
        self.logger.info(f"RandomNumberGenerator initialized with coordinate: {self._coordinate}")
    CONST_A = 8191
    CONST_C = 524287
    CONST_M = 6700417
    CONST_MIN_VAL = 0
    CONST_MAX_VAL = 6700417


    def _get_forecast_url(self, coordinate: Tuple[float, float]) -> str:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coordinate[0]}&longitude=120&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation&wind_speed_unit=ms&temperature_unit=fahrenheit"
        return url

    async def _get_random_seed(self) -> None:
        """Create and store the random seed."""
        try:
            forecast_url = self._get_forecast_url(self._coordinate)
            response = requests.get(forecast_url)
            response.raise_for_status()
            parsed_context = json.loads(response.content)
            self._seed = parsed_context["current"]["temperature_2m"]
            # rotate lat, long coordinates
            lat = (self._coordinate[0] + 10) % 180
            long = (self._coordinate[1] + 10) % 180
            self._coordinate = (lat, long)
            return
        except requests.exceptions.HTTPError as err:
            self.logger.error(f"HTTP error occurred: {err.response.text}")
        except requests.exceptions.RequestException as err:
            self.logger.error(f"Request error occurred: {err}")
        except Exception as err:
            self.logger.error(f"Unexpected error occurred: {err}")

    async def random(self) -> float:
        """Generate a random seed between 0 and 1 using linear congruential generator."""
        if self._seed == 0:
            await self._get_random_seed()
        self._seed = (self.CONST_A * self._seed + self.CONST_C) % self.CONST_M
        return self._seed / self.CONST_MAX_VAL

async def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    generator = RandomNumberGenerator()
    for _ in range(5):
        random_value = await generator.random()
        logging.info(f"Generated random value: {random_value}")
        # Simulate a delay
        import time
        time.sleep(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
