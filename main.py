# Problem 76:
#     Counting Summations
#
# Description:
#     It is possible to write five as a sum in exactly six different ways:
#         4 + 1
#         3 + 2
#         3 + 1 + 1
#         2 + 2 + 1
#         2 + 1 + 1 + 1
#         1 + 1 + 1 + 1 + 1
#
#     How many different ways can one hundred be written as a sum of at least two positive integers?

# Triangular grid to keep track of partitions counted
# PARTITION_WAYS[i][j] is the
#   number of ways to partition `i`
#   where the parts cannot exceed `j+1`.
# No partitions exist where max part is 0, which is why `j` is shifted.
PARTITION_COUNTS = []


def partition_count(n, max_part=None):
    """
    Returns the number of partitions of `n`
      where the parts in any such partition do not exceed `max_part`.
    Note that this also includes partitions having no parts of size `max_part`.

    Args:
        n        (int): Non-negative integer
        max_part (int): Maximum allowed value of any part

    Returns:
        (int): Number of partitions of `n` having maximum part value at most `max_part`.

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n >= 0
    assert max_part is None or type(max_part) == int and max_part >= 0
    # No partitions of `n` having parts greater than `n` itself.
    # So just skip down to `max_part` as `n`, as that's the desired answer anyway.
    max_part = max(1, min(n, max_part or n))

    # Idea:
    #     Attempt to use `max_part` as much as possible to achieve `n`.
    #     Siphon off `max_part` one-by-one, using smaller coins to fill the gap.
    #     To avoid redundant computation, maintain computed counts in `PARTITION_COUNTS`

    global PARTITION_COUNTS
    if n < len(PARTITION_COUNTS) and max_part-1 < len(PARTITION_COUNTS[n])\
            and PARTITION_COUNTS[n][max_part-1] is not None:
        # Already computed this
        return PARTITION_COUNTS[n][max_part-1]
    else:
        # Haven't computed this case yet
        # Extend triangular grid with empty/null values to avoid indexing issues
        PARTITION_COUNTS += [[] for _ in range(n+1-len(PARTITION_COUNTS))]
        PARTITION_COUNTS[n] += [None for _ in range(max_part-len(PARTITION_COUNTS[n]))]

        if n == 0:
            # Technically this doesn't make sense,
            #   but let it vacuously be 1 to satisfy later partition-counting
            ways = 1
        elif max_part == 1:
            # Only one such partition, which is simply (1+...+1), i.e. `1` added `n` times
            ways = 1
        else:
            # Use as much of `max_part` as possible
            next_max_part = max_part - 1
            ways = 0
            max_part_count_max, remaining_sum = divmod(n, max_part)
            for _ in range(max_part_count_max, -1, -1):
                ways += partition_count(remaining_sum, next_max_part)
                remaining_sum += max_part  # Siphon off one `max_part`
        PARTITION_COUNTS[n][max_part-1] = ways
        return ways


def main(n):
    """
    Returns the number of ways to express `n` as an unordered sum of at least two positive integers.
    For example, 1+2 and 2+1 are considered the same sum.

    Args:
        n (int): Natural number

    Returns:
        (int): p(n)-1, where p(n) is the number of partitions of `n`

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n > 0

    # Idea:
    #     Refer to [https://en.wikipedia.org/wiki/Partition_(number_theory)]
    #     Essentially just counting the number of partitions of `n`.
    #     Only modification is that there must be at least two parts,
    #       meaning the partition of `n` into just one part, (n), is not counted,
    #       and there is only one such partition for a given `n`.
    #     If `p(n)` is the number of partitions of `n`,
    #       then this function should return `p(n)-1`.
    #
    #     There is no known formula which exactly computes p(n).
    #     So instead we will use a dynamic program to count the number of partitions of `n`
    #       by using lesser partitions.
    #
    #     The solution will be similar to that of Project Euler Problem #31: Coin Sums.
    #     Refer to [https://projecteuler.net/problem=31]
    #     Only modification is that 'coins' here can have any positive value,
    #       rather than some constrained set of values.

    return partition_count(n)


if __name__ == '__main__':
    sum_total = int(input('Enter a natural number: '))
    sum_partition_count = main(sum_total)
    print('Number of partitions of {}:'.format(sum_total))
    print('  {}'.format(sum_partition_count))
    print('Number of ways to write {} as a sum of at least two positive integers:'.format(sum_total))
    print('  {}'.format(sum_partition_count-1))
