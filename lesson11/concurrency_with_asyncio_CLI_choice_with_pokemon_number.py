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
    try:
        print(f"requesting {url} (requests)")
        response: dict = requests.get(url).json()
        return response["name"]
    except requests.RequestException as e:
        print(f"Error with URL {url}: {e}")
        return e

def sync_pokemons(count: int):
    urls: list[str] = get_urls(n=count)
    results = [http_request(url) for url in urls]
    return results


async def ahttp_request(url: str, session: aiohttp.ClientSession) -> str:
    try:
        print(f"requesting {url} (aiohttp)")
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            return data.get("name")
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print(f"Error with URL {url}: {e}")
        return e


async def async_pokemons(count: int, concurrency: int):
    urls = get_urls(n=count)
    semaphore = asyncio.Semaphore(concurrency)

    async def limited_ahttp_request(url, session):
        async with semaphore:
            return await ahttp_request(url, session)

    async with aiohttp.ClientSession() as session:
        tasks = [limited_ahttp_request(url, session) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


def main():
    parser = argparse.ArgumentParser(description="Fetch Pokémon data using requests or aiohttp.")
    parser.add_argument(
        "client",
        choices=["requests", "aiohttp"],
        help="Specify which HTTP client to use: requests (synchronous) or aiohttp (asynchronous).",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=50,
        help="Specify the number of Pokémon to fetch (default: 50).",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=10,
        help="Specify the number of concurrent requests for aiohttp (default: 10).",
    )
    args = parser.parse_args()

    print(f"You chose: {args.client}")
    print(f"Pokémon count: {args.count}")
    if args.client == "aiohttp":
        print(f"Concurrency: {args.concurrency}")

    start = time.perf_counter()

    if args.client == "requests":
        results = sync_pokemons(count=args.count)
    elif args.client == "aiohttp":
        results = asyncio.run(async_pokemons(count=args.count, concurrency=args.concurrency))
    else:
        raise ValueError("Invalid client specified")

    end = time.perf_counter()

    print(results)
    print(f"The length of the collection: {len(results)}")
    print(f"Execution time: {end - start:.2f} seconds")


if __name__ == "__main__":
    raise SystemExit(main())

# requests --count 200
# aiohttp --count 200 --concurrency 10