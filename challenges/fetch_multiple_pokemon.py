import asyncio
import aiohttp
import json
from typing import Any
from constants import pokemon_list
from fetch_pokemon import print_json
from time import perf_counter


def format_endpoint_url(pokemon_name: str) -> str:
    return f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'

async def fetch_pokemon_data(semaphore, session, endpoint) -> dict[str, Any]:
    
    timeout = aiohttp.ClientTimeout(total=10)
    async with semaphore:
        async with session.get(endpoint, timeout=timeout) as resp:
            resp.raise_for_status() # this will be returned
            
            return await resp.json()

async def fetch_multiple_pokemon(session: aiohttp.ClientSession, pokemon_list: list) -> list[dict[str, Any]]:
    semaphore = asyncio.Semaphore(5) # limit to 5 concurrent requests at any given time

    tasks = [fetch_pokemon_data(semaphore, session, format_endpoint_url(pokemon)) for pokemon in pokemon_list]
    
    start = perf_counter()
    result: list = await asyncio.gather(*tasks, return_exceptions=True)
    print(f'time taken: {(perf_counter() - start):4f}')

    parsed_data = []
    print('--------')
    
    for response_data in result:
        if isinstance(response_data, Exception) or response_data is None:
            continue

        response_data = {'name': response_data.get('name'),
                         'height': response_data.get('height'),
                         'weight': response_data.get('weight'),
                         'base_experience': response_data.get('base_experience')
                        }
        parsed_data.append(response_data)
    
    return parsed_data


async def main():
    
    async with aiohttp.ClientSession() as session:
        data = await fetch_multiple_pokemon(session, pokemon_list)
        
        print(data)


if __name__ == "__main__":
    asyncio.run(main())