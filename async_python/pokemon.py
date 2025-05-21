import asyncio
from typing import Any

import httpx

from utils import time_execution_sync, time_execution_async


BASE_URL = "https://pokeapi.co/api/v2/pokemon/"


# Synchronous

def get_pokemon_data(id: int):
    resp = httpx.get(BASE_URL + str(id))
    resp.raise_for_status()
    return resp.json()


@time_execution_sync
def get_pokemon_sync():
    poke_data = []
    for i in range(1, 151 + 1):
        poke_data.append(get_pokemon_data(i))
    return poke_data


print("sync")
poke_data = get_pokemon_sync()
print(len(poke_data))
print([pokemon["name"] for pokemon in poke_data])


# Asynchronous

async def get_pokemon_data_async(client: httpx.AsyncClient, id: int) -> dict[str, Any]:
    resp = await client.get(BASE_URL + str(id))
    resp.raise_for_status()
    return resp.json()


@time_execution_async
async def get_pokemon_async():
    async with httpx.AsyncClient() as client:
        poke_data = await asyncio.gather(*[
            get_pokemon_data_async(client, i)
            for i in range(1, 151 + 1)
        ])
    return poke_data


print("async")
poke_data = asyncio.run(get_pokemon_async())
print(len(poke_data))


# Asynchronous without gather

@time_execution_async
async def get_pokemon_async_without_gather():
    poke_data = []
    async with httpx.AsyncClient() as client:
        for i in range(1, 151 + 1):
            pokemon_data = await get_pokemon_data_async(client, i)
            poke_data.append(pokemon_data)
    return poke_data


print("async without gather")
poke_data = asyncio.run(get_pokemon_async_without_gather())


# Asynchronous with limit using Sempahore

SEM = asyncio.Semaphore(10)

async def safe_get_pokemon_data(client: httpx.AsyncClient, id: int):
    async with SEM:
        return await get_pokemon_data_async(client, id)


@time_execution_async
async def get_pokemon_async_with_limit():
    async with httpx.AsyncClient() as client:
        poke_data = await asyncio.gather(*[
            safe_get_pokemon_data(client, i)
            for i in range(1, 151 + 1)
        ])
    return poke_data


print("async with semaphore")
poke_data = asyncio.run(get_pokemon_async_with_limit())
print(len(poke_data))
