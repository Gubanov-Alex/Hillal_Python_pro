import random
from statistics import mean
from multiprocessing import Pool,cpu_count
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

    numbers = t1_gen_numbers(10000000)

    with Pool(cpu_count()) as pool:
        results_sum = pool.apply_async(t2_sum_numbers, (numbers,))
        results_avg = pool.apply_async(t3_average_numbers,(numbers,))

        print(results_sum.get())
        print(results_avg.get())

if __name__ == "__main__":
    with TimerContext():
        main()
