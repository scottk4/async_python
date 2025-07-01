import asyncio
from typing import Any
from constants import POKEMON_PER_PAGE

def format_poke_offset(offset: int) -> str:
    return f'https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={POKEMON_PER_PAGE}'

def format_poke_name(name: str) -> str:
    return f'https://pokeapi.co/api/v2/pokemon/{name}'


async def fetch_poke_endpoint(sess, formatted_endpoint: str) -> dict:
    """Shared fetching function for formatted ennpoints"""
    async with sess.get(formatted_endpoint) as resp:
        if resp.status != 200:
            resp.raise_for_status()
        return await resp.json()


async def fetch_all_names(sess, offsets):
    tasks = [asyncio.create_task(fetch_poke_endpoint(sess, format_poke_offset(offset))) for offset in offsets]

    pages = await asyncio.gather(*tasks)
    names = []
    for page in pages:
        names.extend([pokemon['name'] for pokemon in page['results']])
    return names


async def fetch_all_details(sess, names):
    tasks = [asyncio.create_task(fetch_poke_endpoint(sess, format_poke_name(name))) for name in names]

    return await asyncio.gather(*tasks)

