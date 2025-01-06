import random
from time import perf_counter
from statistics import mean
from lesson10.Timer import TimerContext


def t1_gen_numbers(length: int)->list:
    """Generate numbers"""
    return [random.randint(1, 100) for _ in range(length)]


def t2_sum_numbers(numbers:list)->int:
    """Reicieve numbers and calculate their sum"""
    return sum(numbers)


def t3_average_numbers(numbers:list)->float:
    """Wait for numbers and calculate their average"""
    return mean(numbers)

def main ():
    length = 10000000

    start = perf_counter()
    numbers = t1_gen_numbers(length)
    end = perf_counter()
    print(f"\n🕓Time running T1: {end - start:5f} seconds")


    start = perf_counter()
    print(f"\nResult T2: {t2_sum_numbers(numbers):5f}")
    end = perf_counter()
    print(f"\n🕓Time running T2: {end - start:5f} seconds")

    start = perf_counter()
    print(f"\nResult T3: {t3_average_numbers(numbers):5f}")
    end = perf_counter()
    print(f"\n🕓Time running T3: {end - start:5f} seconds")


if __name__ == "__main__":
    with TimerContext():
        main()
