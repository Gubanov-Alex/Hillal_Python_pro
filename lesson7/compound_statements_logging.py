import time
import logging
import  math



class TimerContext:
    """
    Measures the execution time of code inside the with block.
    Uses time.time() to measure time in seconds from the epoch.
    Provides INFO level logs with timestamps, making it suitable for debugging or tracking program execution.
    """
    def __enter__(self):
        self.start_time = time.time()
        logging.info("Start Point")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()
        result_time = self.end_time - self.start_time
        logging.info(f"Finish Point. Used time: {result_time:} second")

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

with TimerContext():
    time.sleep(2)

with TimerContext():
    result = math.factorial(15)
    logging.info(f"Result: {result}")

with TimerContext():
    result = math.fsum(range(1, 7777))
    logging.info(f"Result: {result}")


def test_function_in_timer_context(func, *args, **kwargs):
    """
    Checks the execution of the specified function inside the TimerContext time manager.

    :param func: function to be tested
    :param args: positional arguments for the function
    :param kwargs: named arguments for the function
    """
    with TimerContext():
        result = func(*args, **kwargs)
        logging.info(f"Function `{func.__name__}` executed successfully.")
    return result

test_function_in_timer_context(math.factorial, 15)

group: list[str] = [
    "John",
    "John",
    "Marry",
    "John",
    "Marry",
    "Marry",
    "John",
    "Marry",
    "John",
    "Mark",
    "Mark",
    "Marry",
    "Mark",
] * 100

def deduplicate_generator(data: list[str]):
    filtered_names: set[str] = set()
    for student in data:
        if student not in filtered_names:
            yield student
            filtered_names.add(student)

print('\nGenerator')
for student in deduplicate_generator(group):
    print(f'{20 * '='} \n{student}')

test_function_in_timer_context(deduplicate_generator, group)


def deduplicate_set(data: list[str]):
    filtered_names = set(data)
    return filtered_names

print('\nSet')
for student in deduplicate_set(group):
    print(f'{20 * '='} \n{student}')

test_function_in_timer_context(deduplicate_set, group)

def deduplicate_classic(data: list[str]):
    filtered_names = []
    for student in data:
        if student not in filtered_names:
            filtered_names.append(student)
    return filtered_names

print('\nClassic')
for student in deduplicate_classic(group):
    print(f'{20 * '='} \n{student}')

test_function_in_timer_context(deduplicate_classic, group)
