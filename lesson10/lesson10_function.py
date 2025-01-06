import math
import logging
from lesson10.Timer import TimerContext
from multiprocessing import Process,Queue,cpu_count
from lesson10.lesson10_function_optimus_prod_apply import process_optimize_optimus_aplly
from lesson10_function_optimus_prod import process_optimize_optimus


def get_primes_amount_simple(num: list) -> int:
    result = 0
    for i in num:
        counter = 0
        for j in range(1, i+1):
            if i % j == 0:
                counter += 1
            if counter > 2:
                break

        if counter == 2:
            result += 1

    return result


def get_primes_amount_and_send(num: list, queue: Queue) -> None:
    result = get_primes_amount_simple(num)
    queue.put(result)


def process_optimize(num: list) -> int:
    n_processes = cpu_count()
    logging.info(f"CPU count: {cpu_count()}")
    chunk_size = math.ceil(len(num) / n_processes)
    numbers_chunks = [num[i:i + chunk_size] for i in range(0, len(num), chunk_size) if num[i:i + chunk_size]]

    processes = []
    queue = Queue()

    for chunk in numbers_chunks:
        process = Process(target=get_primes_amount_and_send, args=(chunk, queue))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    total_result = sum(queue.get() for _ in range(len(processes)))
    return total_result


if __name__ == "__main__":

    logging.info(f"Function: get_primes_amount_simple")
    with TimerContext():
        print(get_primes_amount_simple(list(range(1,50000))))

        logging.info(f"Function: process_optimize")

    with TimerContext():
        print(process_optimize(list(range(1,50000))))

    logging.info(f"Function: process_optimize_optimus")
    with TimerContext():
        print(process_optimize_optimus(list(range(1,50000))))

    logging.info(f"Function: process_optimize_optimus_aplly")
    with TimerContext():
        print(process_optimize_optimus_aplly(list(range(1, 50000))))