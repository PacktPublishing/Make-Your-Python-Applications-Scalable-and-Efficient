import timeit

LOOP_VALUE = 1_000_000


def run_for() -> int:
    resp = 0
    for index in range(LOOP_VALUE):
        resp += index
    return resp


def run_while() -> int:
    resp = 0
    index = 0
    while index < LOOP_VALUE:
        resp += index
        index += 1
    return resp


if __name__ == '__main__':
    print('for execution  : ', timeit.timeit(run_for, number=5))
    print('while execution: ', timeit.timeit(run_while, number=5))
