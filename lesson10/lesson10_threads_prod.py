import random
from statistics import mean
from threading import Thread, Event
from lesson10.Timer import TimerContext


def t1_gen_numbers(length: int, numbers: list, num_ready: Event):
    """Generate numbers"""
    numbers.extend(random.randint(1, 100) for _ in range(length))
    num_ready.set()

def t2_sum_numbers(numbers:list, num_ready:Event, result:list):
    """Wait for numbers and calculate their sum"""
    num_ready.wait()
    result.append(sum(numbers))

def t3_average_numbers(numbers:list,num_ready: Event, result:list):
    """Wait for numbers and calculate their average"""
    num_ready.wait()
    result.append(mean(numbers))


def main():
    length = 10000000
    numbers= []
    sum_result = []
    avg_result = []
    num_ready = Event()

    threads = [
    Thread (target=t1_gen_numbers, args=(length,numbers,num_ready)),
    Thread (target=t2_sum_numbers, args=(numbers, num_ready,sum_result)),
    Thread (target=t3_average_numbers, args=(numbers,num_ready,avg_result))
    ]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print(f"\nResult T2 (Sum): {sum_result[0]}")
    print(f"\nResult T3 (Average): {avg_result[0]}")


if __name__ == "__main__":
    with TimerContext():
        main()