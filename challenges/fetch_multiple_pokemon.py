import asyncio
import aiohttp
import json
from typing import Any

from fetch_pokemon import print_json

def format_endpoint_url(pokemon_name: str) -> str:
    return f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'

async def fetch_pokemon_data(session, endpoint) -> dict[str, Any] | None:
    try:
        async with session.get(endpoint) as resp: # add error handling
            if resp.status == 200:
                return await resp.json()
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
    tasks = [asyncio.create_task(
                fetch_pokemon_data(session, format_endpoint_url(pokemon))
            ) for pokemon in pokemon_list]
    
    result: list = await asyncio.gather(*tasks, return_exceptions=True)

    parsed_data = []
    for response_data in result:
        if isinstance(response_data, Exception) or response_data is None:
            continue

        response_data = {'name': response_data['name'],
                         'height': response_data['height'],
                         'weight': response_data['weight'],
                        }
        parsed_data.append(response_data)
    
    print(parsed_data)
    return parsed_data


async def main():
    
    async with aiohttp.ClientSession() as session:
        await fetch_multiple_pokemon(session, ["pikachu2", "charizard", "bulbasaur"])


if __name__ == "__main__":
    asyncio.run(main())