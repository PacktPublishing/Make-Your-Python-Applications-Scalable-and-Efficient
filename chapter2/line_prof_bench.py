LOOP_VALUE = 1_000_000


@profile
def run_for() -> int:
    resp = 0
    cursor = 0
    for index in range(LOOP_VALUE):
        resp += index
        cursor += 1
    return resp


@profile
def run_while() -> int:
    resp = 0
    index = 0
    while index < LOOP_VALUE:
        resp += index
        index += 1
    return resp


if __name__ == '__main__':
    run_for()
    run_while()
