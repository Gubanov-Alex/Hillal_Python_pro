import aiohttp
import asyncio
import time
import random

BASE_URL = "https://pokeapi.co/api/v2/pokemon/{pokemon_id}"


async def ahttp_request(url: str) -> str:
    print(f"requesting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data["name"]


def get_urls(n: int) -> list[str]:
    return [BASE_URL.format(pokemon_id=random.randint(1, 500)) for _ in range(n)]


async def async_pokemons():
    urls: list[str] = get_urls(n=50)
    tasks = [ahttp_request(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


def main():
    start = time.perf_counter()
    data = asyncio.run(async_pokemons())
    end = time.perf_counter()
    print(data)
    print(f"the len of the collection: {len(data)}")
    print(f"execution time: {end - start}")


if __name__ == "__main__":
    raise SystemExit(main())