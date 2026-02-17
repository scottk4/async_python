# Async Pokémon Fetcher
A high-performance Python utility for fetching Pokémon data from the PokeAPI. This project demonstrates professional asynchronous patterns, including rate-limiting with Semaphores and robust error handling.

## Features
Concurrency: Fetches multiple Pokémon simultaneously using asyncio and aiohttp.

Rate Limiting: Uses an asyncio.Semaphore to prevent overwhelming the API and getting rate-limited.

Robust Error Handling: Utilizes raise_for_status() to gracefully handle HTTP errors (404, 500, etc.) without crashing.

Non-Blocking: Leverages the async/await syntax for maximum I/O efficiency.

### Installation
Clone the repository:

Bash
git clone https://github.com/yourusername/pokemon-async-fetcher.git
cd pokemon-async-fetcher
**Install dependencies**:
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

## Usage
Ensure you have a constants.py file with a pokemon_list and run the main script:

Bash
python main.py
How it Works
The script initializes an aiohttp.ClientSession and creates a batch of tasks. The Semaphore acts as a traffic controller:

If the Semaphore is set to 5, only 5 requests are active at once.

As one request finishes, the next one in the queue begins.

The asyncio.gather(return_exceptions=True) call ensures that if one request fails (e.g., a 404), the rest of the batch continues uninterrupted.