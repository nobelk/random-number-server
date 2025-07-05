
import time
import logging

from RandomNumberGenerator import RandomNumberGenerator


async def test_random_number_generation() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    generator: RandomNumberGenerator = RandomNumberGenerator()
    logger.info("Starting random number generation test")
    
    for i in range(5):
        random_value: float = await generator.random()
        logger.info(f"Test {i+1}: Generated value {random_value}")
        assert random_value >= 0 and random_value <= 1, f"Random value {random_value} out of bounds"
        # Simulate a delay
        time.sleep(1)
    
    logger.info("Random number generation test completed successfully")
