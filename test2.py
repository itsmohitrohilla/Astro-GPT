from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
import time  # For calculating response time
    
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
    
from redis import asyncio as aioredis
    
test_app = FastAPI()

# Simulate a time-consuming mathematical operation
def long_math_task(a: int, b: int):
    result = 0
    for i in range(1, 10000000):
        result += a * b  # Repeated multiplication
    return result

# API route to accept two numbers as query parameters
@test_app.get("/calculate")
@cache(expire=100)
async def calculate(a: int, b: int):
    # Start timer
    start_time = time.time()

    # Perform the long mathematical task
    result = long_math_task(a, b)

    # Calculate response time
    response_time = time.time() - start_time
    print(f"Response Time: {response_time} seconds")  # Print response time to terminal

    # Return the result and response time
    return dict(result=result, response_time=response_time)

@test_app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
