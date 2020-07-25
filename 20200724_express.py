""" Solves the July 24 2020 Riddler Express, https://fivethirtyeight.com/features/are-you-a-pinball-wizard/ """
import itertools


def possibilities():
    """
    Generates all of the subsets of the set of shires, where both:
    a - the total number of votes in the subset is sufficiently high, and
    b - every member of the subset is needed to make the total
    """
    shire_seats = {i for i in range(3, 13)}
    # No set of three or fewer shires has enough votes.
    # No set of eight or more needs its smallest member.
    for s in range(4, 8):
        for subset in itertools.combinations(shire_seats, s):
            subset_sum = sum(subset)
            if subset_sum > 37:
                subset_min = min(subset)
                if subset_sum - subset_min < 38:
                    yield subset


def main():
    total_pop = sum(((10 * (i - 2)) + 1) for i in range(3, 13))
    min_votes_to_win_seats = {i: (((i - 2) * 5) + 1) for i in range(3, 13)}
    min_winning_population = total_pop
    for this_possibility in possibilities():
        possibility_min = \
            sum(min_votes_to_win_seats[i] for i in this_possibility)
        if possibility_min < min_winning_population:
            min_winning_population = possibility_min

    print('Lowest proportion = ' + \
          str(min_winning_population) + ' / ' + str(total_pop))
    percentage = "{:.2%}".format(min_winning_population / total_pop)
    print(' = ' + percentage)


if __name__ == "__main__":
    main()
