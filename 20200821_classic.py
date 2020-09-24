import math


def main():
    min_n = 3
    answers = dict()
    for kk in range(333, 0, -1):
        k = kk / 1000
        max_n = math.floor(1 / k)
        answers[k] = dict()
        for n in range(min_n, max_n+1):
            perimeter = 1 - (n * k)
            side_length = perimeter / n
            tan_ratio = math.tan(math.pi / n)
            total_area = 0.25 * n * side_length * side_length / tan_ratio
            answers[k][n] = total_area
    for k, poss in answers.items():
        print(str(k) + ' : ' + str(poss))


if __name__ == '__main__':
    main()
