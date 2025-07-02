import asyncio
import aiohttp
from time import perf_counter
from fetch_pokemon import print_json
from constants import POKEMON_PER_PAGE
from typing import Any

def format_name_offsets(offset):
    return f'https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={POKEMON_PER_PAGE}'

async def get_pokemon_count(session):
    async with session.get(format_name_offsets(0)) as resp:
        data = await resp.json()
        return data['count']

async def fetch_poke_page(semaphore, session, endpoint) -> None | dict[str, Any]:
    async with semaphore:
        try:
            async with session.get(endpoint) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result

                elif resp.status == 404:
                    print(f'Invalid endpoint: {endpoint}')
                else:
                    print(f"Failed to get endpoint with status: {resp.status}")
        
        except aiohttp.ClientError as e:
            print(f"network/client error: {e}")
    
    return None

def parse_name_from_page(page_response) -> list:
    names = []
    for result in page_response["results"]:
        names.append(result['name'])
    return names

async def fetch_all_pokemon_names(session):
    pokemon_count = await get_pokemon_count(session)
    endpoints = [format_name_offsets(offset) for offset in range(0, pokemon_count, POKEMON_PER_PAGE)]
    
    semaphore = asyncio.Semaphore(3)

    task_coroutines = [
        fetch_poke_page(semaphore, session, endpoint) for endpoint in endpoints
    ]
    # start_time = perf_counter()
    results = await asyncio.gather(*task_coroutines)
    # print(f'total time taken (s): {perf_counter() - start_time}')

    pokemon_names = []
    for page in results:
        if page is None:
            continue
        else:
            page_names = parse_name_from_page(page)
            pokemon_names += page_names
    
    # print('num of pokes fetched: ', len(pokemon_names))
    return pokemon_names

async def main():

    async with aiohttp.ClientSession() as session:
        await fetch_all_pokemon_names(session)

if __name__ == "__main__":
    asyncio.run(main())
