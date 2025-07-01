## Asyncio tutorial for making requests

Async programming is best when we need to wait for tasks to finish. The importance is to understand that coroutines are not executed until they are awaited.

```
async def fetch_data(delay):
    print("Fetching data...")
    await asyncio.sleep(delay) ## simulate I/O operation
    print("data fetched")
    return {"data", "Some data"} # return some data

# coroutine function
async def main():
    print('start of main coroutine')
    task = fetch_data(2) # not yet gets executed, returns coroutine very important
```

There is no improvement in this function because the data runs syncrounsly since each task is awaited individually

```
async def main():
    task1 = fetch_data(2,1)
    task2 = fetch_data(2,2)

    result1 = await task1 # start executing task1
    print(f"Received result: {result1}")

    result2 = await task2 # start executing task2
    print(f"Received result: {result2}")
```

This creates all the tasks on the event loop at the same time


```
async def fetch_data(id, sleep_time):
    print(f"Coroutine {id} starting to fetch data.")
    await asyncio.sleep(sleep_time)
    return {"id": id, "data": f'sample data from coroutine {id}'}


async def main():
    start_time = perf_counter()

    task1 = asyncio.create_task(fetch_data(1,2))
    task2 = asyncio.create_task(fetch_data(2,3))
    task3 = asyncio.create_task(fetch_data(3,1))
```

this is shorter notation using ```asyncio.gather``` not the easiest for error handling.
```
results = await asyncio.gather(fetch_data(1,2), fetch_data(2,3), fetch_data(3,1))
```

Using a task group is better for error handling:
```
tasks = []
    # will create and execute each task con-currently
    async with asyncio.TaskGroup() as tg: # will cancel all tasks if one fails - better error handling
        for i, sleep_time in enumerate([2,1,3], start=1):
            task = tg.create_task(fetch_data(i, sleep_time))
            tasks.append(task)
```