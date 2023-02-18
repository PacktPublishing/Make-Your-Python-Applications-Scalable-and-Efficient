def fibonacci(value: int) -> int:
    a = 0
    b = 1
    if value in {a, b}:
        return value
    for _ in range(1, value):
        c = a + b
        a = b
        b = c
    return b
