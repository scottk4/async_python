# Async Pokémon Fetcher
A Python utility for fetching Pokémon data from the PokeAPI. This project helped was developed to help me learn asynchronous patterns, including rate-limiting with Semaphores and error handling.

## Features
Concurrency: Fetches multiple Pokémon simultaneously using asyncio and aiohttp.

Rate Limiting: Uses an asyncio.Semaphore to prevent overwhelming the API and getting rate-limited.

Non-Blocking: Uses the async/await syntax for maximum I/O efficiency.

### Installation
Clone the repository:

```git clone https://github.com/scottk4/async_python.git```

**Install dependencies**:

```python3 -m venv venv```

```source venv/bin/activate```

```pip install -r requirements.txt```

```cd challenges```

## Usage

Update the ```pokemon_list``` in ```constants.py``` with a list of pokemon you want to get data for.

then run:

```python3 fetch_multiple_pokemon.py```

## How it Works

The script initializes an aiohttp.ClientSession and creates a batch of tasks. The Semaphore acts as a traffic controller:

If the Semaphore is set to 5, only 5 requests are active at once.

As one request finishes, the next one in the queue begins.

The asyncio.gather(return_exceptions=True) call ensures that if one request fails (e.g., a 404), the rest of the batch continues uninterrupted.
