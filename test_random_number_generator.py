
import time

from RandomNumberGenerator import RandomNumberGenerator


async def test_random_number_generation():
    generator = RandomNumberGenerator()
    for _ in range(5):
        random_value = await generator.random()
        assert random_value >= 0 and random_value <= 1, "Random value out of bounds"
        # Simulate a delay
        time.sleep(1)
