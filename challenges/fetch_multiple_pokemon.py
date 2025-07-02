import asyncio
import aiohttp
import json
from typing import Any
from constants import pokemon_list
from fetch_pokemon import print_json
from time import perf_counter

def format_endpoint_url(pokemon_name: str) -> str:
    return f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'

async def fetch_pokemon_data(semaphore, session, endpoint) -> dict[str, Any] | None:
    async with semaphore:
        try:
            async with session.get(endpoint) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # print(f'fetched: {data['name']}')
                    return data
                elif resp.status == 404:
                    # raise Exception(f'pokemon not found: {endpoint}')
                    print(f'pokemon not found: {endpoint}')
                else:
                    # raise Exception(f'failed to get request: {endpoint}')
                    print(f'failed to get request: {endpoint}')
                
        except aiohttp.ClientError as e:
            # raise Exception(f'client error {e}')
            print(f'client error {e}')
        
        return None


async def fetch_multiple_pokemon(session, pokemon_list: list) -> list[dict[str, Any]]:
    semaphore = asyncio.Semaphore(20) # limit to 5 concurrent requests

    tasks = [asyncio.create_task(
                fetch_pokemon_data(semaphore, session, format_endpoint_url(pokemon))
            ) for pokemon in pokemon_list]
    
    start = perf_counter()
    result: list = await asyncio.gather(*tasks, return_exceptions=True)
    print(f'time taken: {(perf_counter() - start):4f}')

    parsed_data = []
    print('--------')
    for response_data in result:
        if isinstance(response_data, Exception) or response_data is None:
            continue

        response_data = {'name': response_data['name'],
                         'height': response_data['height'],
                         'weight': response_data['weight'],
                         'base_experience': response_data['base_experience']
                        }
        parsed_data.append(response_data)
    
    return parsed_data


async def main():
    
    async with aiohttp.ClientSession() as session:
        await fetch_multiple_pokemon(session, pokemon_list)


if __name__ == "__main__":
    asyncio.run(main())