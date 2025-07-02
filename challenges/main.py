import asyncio
import aiohttp
from fetch_poke_names import fetch_all_pokemon_names
from fetch_multiple_pokemon import fetch_multiple_pokemon
from sort_data import make_dataframe
async def main():

    async with aiohttp.ClientSession() as session:
        all_pokemon_names = await fetch_all_pokemon_names(session)
        all_pokemon_data = await fetch_multiple_pokemon(session, all_pokemon_names)
    
    df = make_dataframe(all_pokemon_data, 'base_experience')
    print(df.head(5))

if __name__ == "__main__":
    asyncio.run(main())