from multiprocessing import Pool, cpu_count,Pipe
from lesson10.Timer import TimerContext



def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def get_primes_amount(numbers: list) -> int:
      return sum(1 for i in numbers if is_prime(i))


def split_into_chunks(lst, n):
      for i in range(0, len(lst), n):
        yield lst[i:i + n]


def process_optimize_optimus(numbers: list) -> int:
    chunks = list(split_into_chunks(numbers, len(numbers) // cpu_count() or 1))
    with Pool(cpu_count()) as pool:
        results = pool.map(get_primes_amount, chunks)
    return sum(results)


if __name__ == "__main__":

    with TimerContext():
        print(process_optimize_optimus(list(range(1,5000000))))