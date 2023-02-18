from memory_profiler import profile


@profile(precision=4)
def main() -> None:
    l1 = [value for value in range(1_000_000)]
    print(sum(l1))
    del l1


if __name__ == '__main__':
    main()
