import aiohttp
import asyncio
import time
import random
import requests
import argparse


BASE_URL = "https://pokeapi.co/api/v2/pokemon/{pokemon_id}"


def get_urls(n: int) -> list[str]:
    return [BASE_URL.format(pokemon_id=random.randint(1, 500)) for _ in range(n)]

def http_request(url: str) -> str:
    print(f"requesting {url} (requests)")
    response: dict = requests.get(url).json()
    return response["name"]

def sync_pokemons():
    urls: list[str] = get_urls(n=50)
    results = [http_request(url) for url in urls]
    return results


async def ahttp_request(url: str, session: aiohttp.ClientSession) -> str:
    print(f"requesting {url} (aiohttp)")
    async with session.get(url) as response:
        data = await response.json()
        return data["name"]


async def async_pokemons():
    urls: list[str] = get_urls(n=50)
    async with aiohttp.ClientSession() as session:
        tasks = [ahttp_request(url, session) for url in urls]
        results = await asyncio.gather(*tasks)
    return results



def main():
    parser = argparse.ArgumentParser(description="Fetch Pokémon data using requests or aiohttp.")
    parser.add_argument(
        "client",
        choices=["requests", "aiohttp"],
        help="Specify which HTTP client to use: requests (synchronous) or aiohttp (asynchronous).",
    )
    args = parser.parse_args()
    print(f"You choose: {args.client}")
    start = time.perf_counter()


    if args.client == "requests":
        results = sync_pokemons()
    elif args.client == "aiohttp":
       results = asyncio.run(async_pokemons())
    else:
        raise ValueError("Invalid client specified")

    end = time.perf_counter()

    print(results)
    print(f"The length of the collection: {len(results)}")
    print(f"Execution time: {end - start:.2f} seconds")


if __name__ == "__main__":
    raise SystemExit(main())