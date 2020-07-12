""" Solves the July 10 2020 Riddler Classic, https://fivethirtyeight.com/features/can-you-make-24/ """
import itertools


def stack_valid(stack):
    ret_val = True
    stack_length = len(stack)
    if stack_length > 1:  # a single ring will always fit
        for stack_pos, this_ring in enumerate(stack):
            ring_min_size = stack_length - stack_pos
            if this_ring < ring_min_size:
                ret_val = False
                break
    return ret_val


def non_empty_powerset(size):
    """Yields the non-empty sets that are subsets of the set of ints from 1 to size"""
    big_set = set(range(1, size + 1))
    for n in range(1, size + 1):
        for s in itertools.combinations(big_set, n):
            yield set(s)


def main():
    good = 0
    bad = 0
    for n in non_empty_powerset(5):  # get all the possible sets of rings
        for l in itertools.permutations(n):  # permute each set
            print(str(l))
            if stack_valid(l):
                print('Good')
                good += 1
            else:
                print('Bad')
                bad += 1
    print()
    print('Total good = ' + str(good))
    print('Total bad = ' + str(bad))


if __name__ == "__main__":
    main()
