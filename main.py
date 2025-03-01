import time
import logging
import threading
import random
from concurrent.futures import ThreadPoolExecutor

# Environment variables (should be set in a .env file)
LOGGING_FORMAT = "%(asctime)s | %(levelname)-5s | %(message)s"
LOGGING_LEVEL = logging.DEBUG
MAX_WORKERS = 8

# Configure logging
logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)


class Processor:
    """
    Main class - it doubles each value in a list of integers.
    If data input is not valid, a ValueError is raised before processing.
    If data input is valid, a thread pool is created with a maximum number of workers.
    If the number of items is less than the maximum number of workers, the number of workers is adjusted.
    Otherwise, subsequent items are processed by the available workers.
    """

    def __init__(self, items: list[int]) -> None:
        """
        Initialize the Processor class

        Args:
            items (list[int]): List of integers
        """
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.max_workers: int = min(MAX_WORKERS, len(items))
        self.logger.info(f"Processor initialized with {self.max_workers} workers")
        self.items: list[int] = self.validate_items(items)
        self.logger.info("Data input validated")

    def validate_items(self, items: list[int]) -> list[int]:
        """
        Validate the data input

        Args:
            items (list[int]): List of integers

        Returns:
            list[int]: The validated list of integers

        Raises:
            ValueError: If the data input is not valid
        """
        self.logger.debug(f"Data input: {items}")

        # Assert that the data is a list
        if not isinstance(items, list):
            error_message = "Data must be a list"
            self.logger.error(f"{error_message} - Input: {items}")
            raise ValueError(error_message)
        else:
            self.logger.debug("Data validation: data is a list")

        # Assert that the data is not empty
        if not items:
            error_message = "Data cannot be empty"
            self.logger.error(f"{error_message} - Input: {items}")
            raise ValueError(error_message)
        else:
            self.logger.debug("Data validation: data is not empty")

        # Assert that all items are integers
        for i, item in enumerate(items):
            if not isinstance(item, int):
                error_message = f"Incorrect data type at index {i}"
                self.logger.error(f"{error_message} - Input: {items}")
                raise ValueError(f"{error_message} - all items must be integers")

        self.logger.debug("Data validation: all items are integers")
        return items

    def process_item(self, item: int) -> int:
        """
        Doubles the given item value.

        Args:
            item (int): The integer to be processed.

        Returns:
            int: The doubled value of the input item.
        """
        worker_name = threading.current_thread().name
        time.sleep(0.5)
        result = item * 2
        self.logger.debug(f"Worker: {worker_name} - Input: {item} - Result: {result}")
        return result

    def run_process(self) -> list[int]:
        """
        Create a thread pool and run a process for each item

        Returns:
            list[int]: The list of processed items
        """
        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                return list(executor.map(self.process_item, self.items))
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return []


if __name__ == "__main__":

    # Generate random data
    data_length: int = random.randint(6, 20)
    data: list[int] = [random.randint(-100, 100) for _ in range(data_length)]

    # Initialize the Processor class
    processor = Processor(items=data)

    # Run the process
    output = processor.run_process()
    print(f"\033[92mOutput:\033[0m {output}")
