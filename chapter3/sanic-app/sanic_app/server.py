import random

from sanic import Sanic
from sanic.response import json
from models import fibonacci

app = Sanic("SanicFibonacciApp")


@app.get("/fibonacci/")
async def core(request):
    random_num = random.randint(1, 10)
    data = {
        'random_num': random_num,
        'fib_result': fibonacci(random_num),
    }
    return json(data)
