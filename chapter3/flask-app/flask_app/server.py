import random

from flask import Flask
from models import fibonacci

app = Flask(__name__)


@app.get("/fibonacci/")
def hello_world():
    random_num = random.randint(1, 10)
    return {
        'random_num': random_num,
        'fib_result': fibonacci(random_num),
    }
