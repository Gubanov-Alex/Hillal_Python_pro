import aiohttp
import asyncio
import time
import random
import requests
import argparse


BASE_URL = "https://pokeapi.co/api/v2/pokemon/{pokemon_id}"


def http_request(url: str) -> str:
    print(f"requesting {url}")
    response: dict = requests.get(url).json()
    return response["name"]


async def ahttp_request(url: str) -> str:
    print(f"requesting {url}")
    response: requests.Response = await asyncio.to_thread(requests.patch, url)
    return response.json()["name"]


def get_urls(n: int) -> list[str]:
    return [BASE_URL.format(pokemon_id=random.randint(1, 500)) for _ in range(n)]


def sync_pokemons():
    urls: list[str] = get_urls(n=50)
    results = [http_request(url) for url in urls]

    return results


async def async_pokemons():
    urls: list[str] = get_urls(n=50)
    tasks = [ahttp_request(url) for url in urls]
    results = await asyncio.gather(*tasks)

    return results


def main():

    start = time.perf_counter()
    data = asyncio.run(async_pokemons())
    # sync_data = sync_pokemons()
    end = time.perf_counter()

    # print(sync_data)
    # print(f"the len of the collection: {len(sync_data)}")
    # print(f"execution time: {end - start}")

    print(data)
    print(f"the len of the collection: {len(data)}")
    print(f"execution time: {end - start}")


if __name__ == "__main__":
    raise SystemExit(main())