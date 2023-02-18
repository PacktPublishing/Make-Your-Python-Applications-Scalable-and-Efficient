def main() -> None:
    l1 = []
    for value in range(1_000_000):
        l1.append(value)
    print(sum(l1))


if __name__ == '__main__':
    # Importing libs cProfile and pstats
    import cProfile
    import pstats
    # Collecting statistics using cProfile
    with cProfile.Profile() as p:
        main()
    # Instantiating  pstats using data from cProfile
    stats = pstats.Stats(p)
    # Removing directory names from filename fields
    stats.strip_dirs()
    # Sorting data by total time (tottime)
    stats.sort_stats(pstats.SortKey.TIME)
    # Printing the statistics
    stats.print_stats()
    # Creating file to be read by snakeviz
    stats.dump_stats('out.prof')
