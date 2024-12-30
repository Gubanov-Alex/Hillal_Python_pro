import random
from statistics import mean
import asyncio
from lesson10.Timer import TimerContext



def t1_gen_numbers(length: int)->list:
    """Generate numbers"""
    return [random.randint(1, 100) for _ in range(length)]


async def t2_sum_numbers(numbers:list)->int:
    """Receive numbers and calculate their sum"""
    return sum(numbers)


async def t3_average_numbers(numbers:list)->float:
    """Wait for numbers and calculate their average"""
    return mean(numbers)

async def main ():
    length = 10000000

    numbers = t1_gen_numbers(length)
    print(f"\nResult T2: {await t2_sum_numbers(numbers):5f}")
    print(f"\nResult T3: {await t3_average_numbers(numbers):5f}")


if __name__ == "__main__":
    with TimerContext():
        asyncio.run(main())
