import logging
from time import perf_counter

# Constants
LOG_MESSAGE = "Execution finished. Elapsed time: {:.6f} seconds."


class TimerContext:
    """
    Measures the execution time of code inside the context manager block.
    Logs elapsed time with INFO level by default.
    """

    def __enter__(self):
        self.start_time = perf_counter()
        logging.info("Timer started.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = perf_counter()
        self._log_elapsed_time()

    def _log_elapsed_time(self, log_level=logging.INFO):
        """
        Logs the elapsed time at the specified logging level.
        """
        elapsed_time = self.end_time - self.start_time
        logging.log(log_level, LOG_MESSAGE.format(elapsed_time))


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
