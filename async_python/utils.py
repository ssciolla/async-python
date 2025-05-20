import functools
import time
from typing import Callable


def time_execution_sync(callable: Callable) -> Callable:
    @functools.wraps(callable)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = callable(*args, **kwargs)
        end = time.time()
        delta = end - start
        print(f'{callable.__qualname__} took {delta} seconds to complete.')
        return result

    return wrapper

def time_execution_async(callable: Callable) -> Callable:
    @functools.wraps(callable)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await callable(*args, **kwargs)
        end = time.time()
        delta = end - start
        print(f'{callable.__qualname__} took {delta} seconds to complete.')
        return result

    return wrapper