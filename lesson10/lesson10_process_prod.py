import random
from statistics import mean
from multiprocessing import Process,Queue
from lesson10.Timer import TimerContext


def t1_gen_numbers(length: int)->list:
    """Generate numbers"""
    return [random.randint(1, 100) for _ in range(length)]

def t2_sum_numbers(list,queue)->int:
    """Reicieve numbers and calculate their sum"""
    queue.put(sum(list))

def t3_average_numbers(list,queue)->float:
    """Wait for numbers and calculate their average"""
    queue.put(mean(list))

def main ():

    numbers = t1_gen_numbers(10000000)
    queue = Queue()

    processes = [
        Process(target=t2_sum_numbers, args=(numbers, queue)),
        Process(target=t3_average_numbers, args=(numbers, queue)),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    results = [queue.get() for _ in processes]
    print(f"Results from processes:\nSum Number:{results[0]} \nAvg Number:{results[1]}")


if __name__ == "__main__":
    with TimerContext():
        main()
