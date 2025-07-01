import asyncio
import aiohttp
import json
import pandas as pd
from typing import Any

PAGES = 3
POKEMON_PER_PAGE = 20

def print_json(data):
    print(json.dumps(data, indent=2))

async def fetch_poke_page(sess, offset):
    async with sess.get(f'https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={POKEMON_PER_PAGE}') as resp:
        if resp.status != 200:
            resp.raise_for_status()
        return await resp.json()

async def fetch_poke_details(sess, name):
    async with sess.get(f'https://pokeapi.co/api/v2/pokemon/{name}') as resp:
        if resp.status != 200:
            resp.raise_for_status()
        return await resp.json()


async def fetch_all_names(sess, offsets):
    tasks = [asyncio.create_task(fetch_poke_page(sess, offset)) for offset in offsets]

    pages = await asyncio.gather(*tasks)
    names = []
    for page in pages:
        names.extend([pokemon['name'] for pokemon in page['results']])
    return names


async def fetch_all_details(sess, names):
    tasks = [asyncio.create_task(fetch_poke_details(sess, name)) for name in names]

    details = await asyncio.gather(*tasks)
    return details

def get_poke_name_types(poke_types: list[dict[str, Any]]):
    return [poke_type['type']['name'] for poke_type in poke_types]

def make_dataframe(details):

    details_dict = {'name': [], 'base_experience': [], 'types': [], 'weight': []}
    for poke_detail in details:
        
        details_dict['name'].append(poke_detail['name'])
        details_dict['base_experience'].append(poke_detail['base_experience'])
        details_dict['types'].append(get_poke_name_types(poke_detail['types']))
        details_dict['weight'].append(poke_detail['weight'])

    df = pd.DataFrame(details_dict)
    return df.sort_values(by="base_experience", ascending=False)

async def main():
    offsets = [POKEMON_PER_PAGE * i for i in range(0, PAGES)]
    async with aiohttp.ClientSession() as sess:
        names = await fetch_all_names(sess, offsets)
        details = await fetch_all_details(sess, names)

    df = make_dataframe(details)
    df.head(5).to_csv("top_5_pokemon.csv", index=False)
    


if __name__ == "__main__":
    asyncio.run(main())