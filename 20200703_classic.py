# Answers the Classic from https://fivethirtyeight.com/features/can-you-stay-in-your-lane/


def centred_pentagonals():
    n = 1
    while True:
        yield int(((5 * n * n) + (5 * n) + 2) / 2)
        n += 1


def doubled_squares():
    n = 1
    while True:
        yield 2 * n * n
        n += 1


def main():
    pentagonal_seq = centred_pentagonals()
    squares_seq = doubled_squares()
    this_pentagonal = next(pentagonal_seq)
    this_doubled_square = next(squares_seq)
    while True:
        if (this_pentagonal - 1 == this_doubled_square) and this_pentagonal != 51:
            print(this_doubled_square)
            break
        elif this_pentagonal > this_doubled_square:
            this_doubled_square = next(squares_seq)
        elif this_pentagonal < this_doubled_square:
            this_pentagonal = next(pentagonal_seq)
        elif this_pentagonal == this_doubled_square:
            this_pentagonal = next(pentagonal_seq)
            this_doubled_square = next(squares_seq)


if __name__ == "__main__":
    main()
