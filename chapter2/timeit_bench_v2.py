import timeit

LOOP_VALUE = 1_000_000


def run_for() -> int:
    '''
    1           0 RESUME                   0

    # loading variable resp
    2           2 LOAD_CONST               1 (0)
                4 STORE_FAST               0 (resp)

    # loading variable cursor
    3           6 LOAD_CONST               1 (0)
                8 STORE_FAST               1 (cursor)

    # loading python range using global LOOP_VALUE
    4          10 LOAD_GLOBAL              1 (NULL + range)
                22 LOAD_GLOBAL              2 (LOOP_VALUE)
                34 PRECALL                  1
                38 CALL                     1
                48 GET_ITER
    # Get the next item in the iterator and store it in the 'index' variable
            >>   50 FOR_ITER                12 (to 76)
                52 STORE_FAST               2 (index)

    # sum 'index' value on 'resp' variable
    5          54 LOAD_FAST                0 (resp)
                56 LOAD_FAST                2 (index)
                58 BINARY_OP               13 (+=)
                62 STORE_FAST               0 (resp)

    # sum 1 on 'cursor' variable
    6          64 LOAD_FAST                1 (cursor)
                66 LOAD_CONST               2 (1)
                68 BINARY_OP               13 (+=)
                72 STORE_FAST               1 (cursor)

    # backing to step 50 to validate next item in the iterator
                74 JUMP_BACKWARD           13 (to 50)

    # returning the last value of 'resp' variable
    7     >>   76 LOAD_FAST                0 (resp)
                78 RETURN_VALUE
    '''
    resp = 0
    cursor = 0
    for index in range(LOOP_VALUE):
        resp += index
        cursor += 1
    return resp


def run_while() -> int:
    '''
    1           0 RESUME                   0

    # loading variable resp
    2           2 LOAD_CONST               1 (0)
                4 STORE_FAST               0 (resp)

    # loading variable index
    3           6 LOAD_CONST               1 (0)
                8 STORE_FAST               1 (index)

    # validating if 'index' is minor than global LOOP_VALUE
    4          10 LOAD_FAST                1 (index)
                12 LOAD_GLOBAL              0 (LOOP_VALUE)
                24 COMPARE_OP               0 (<)
                30 POP_JUMP_FORWARD_IF_FALSE    21 (to 74)

    # # sum 'index' value on 'resp' variable
    5     >>   32 LOAD_FAST                0 (resp)
                34 LOAD_FAST                1 (index)
                36 BINARY_OP               13 (+=)
                40 STORE_FAST               0 (resp)

    # sum 1 on 'index' variable
    6          42 LOAD_FAST                1 (index)
                44 LOAD_CONST               2 (1)
                46 BINARY_OP               13 (+=)
                50 STORE_FAST               1 (index)

    # validating if 'index' is minor than global LOOP_VALUE
    4          52 LOAD_FAST                1 (index)
                54 LOAD_GLOBAL              0 (LOOP_VALUE)
                66 COMPARE_OP               0 (<)
                72 POP_JUMP_BACKWARD_IF_TRUE    21 (to 32)

    # returning the last value of 'resp' variable
    7     >>   74 LOAD_FAST                0 (resp)
                76 RETURN_VALUE
    '''
    resp = 0
    index = 0
    while index < LOOP_VALUE:
        resp += index
        index += 1
    return resp


if __name__ == '__main__':
    print('for execution  : ', timeit.timeit(run_for, number=5))
    print('while execution: ', timeit.timeit(run_while, number=5))
