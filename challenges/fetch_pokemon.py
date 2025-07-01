"""Challenge 1: Fetch a pokemon and print some information about it
                apply error handling if its an invalid pokemon name"""

import asyncio
import aiohttp
import json

def print_json(data: dict):
    print(json.dumps(data, indent=2))

async def fetch_pokemon(sess, pokemon_name):
    try:
        async with sess.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}') as resp:
            if resp.status == 200:
                result = await resp.json()
                print(result['name'])
                print(result['height'])
                print(result['weight'])
            elif resp.status == 404:
                print(f"Pokemon {pokemon_name} not found")
            else:
                print(f"request failed with status: {resp.status}")
            
    except aiohttp.ClientError as e:
        print('Network or client error: {e}')

async def main():
    pokemon = 'charizard2'
    async with aiohttp.ClientSession() as sess:
        await fetch_pokemon(sess, pokemon)


if __name__ == "__main__":
    asyncio.run(main())