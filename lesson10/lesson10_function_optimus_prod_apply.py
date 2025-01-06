from multiprocessing import Pool, cpu_count
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


def process_optimize_optimus_aplly(numbers: list) -> int:
   with Pool(cpu_count()) as pool:
        results = pool.apply(get_primes_amount, (numbers,))
        return  results


if __name__ == "__main__":

    with TimerContext():
        print(process_optimize_optimus_aplly(list(range(1,5000000))))