import itertools
import datetime

SOURCE_FILE = '20200103_input_enable1.txt'


def letter_set(word):
    return {char for char in word}


def get_possible_honeycombs():
    with open(SOURCE_FILE) as f:
        possible_honeycombs = set([frozenset({char for char in this_line}) for this_line in f.read().splitlines()
                                  if 's' not in this_line and len({char for char in this_line}) == 7])
    return possible_honeycombs


def get_relevant_word_list():
    with open(SOURCE_FILE) as f:
        relevant_words = [this_line for this_line in f.read().splitlines()
                          if 's' not in this_line and len(this_line) > 3 and len({char for char in this_line}) < 8]
    return relevant_words


def word_score(word):
    if len(word) == 4:
        return 1
    elif len(letter_set(word)) == 7:
        return 7 + len(word)
    else:
        return len(word)


def main():
    relevant_words = get_relevant_word_list()
    print(str(len(relevant_words)) + ' relevant words')
    possible_honeycombs = get_possible_honeycombs()
    total_honeycombs_to_check = len(possible_honeycombs)
    print(str(total_honeycombs_to_check) + ' possible honeycombs')

    letter_spans = dict()
    for this_word in relevant_words:
        this_word_letters = frozenset(letter_set(this_word))
        if this_word_letters in letter_spans.keys():
            letter_spans[this_word_letters][0] += word_score(this_word)
            letter_spans[this_word_letters][1].append(this_word)
        else:
            letter_spans[this_word_letters] = [word_score(this_word), [this_word]]
    print('Created ' + str(len(letter_spans)) + ' letter span entries.')

    print('Checking coverage')
    i = 0
    for this_letter_span in letter_spans.keys():
        if len(this_letter_span) == 7:
            continue
        else:
            has_superset = False
            for superset_letter_span in letter_spans.keys():
                if this_letter_span < superset_letter_span:
                    has_superset = True
                    break
            if not has_superset:
                i += 1
                possible_honeycombs.add(this_letter_span)
    print('Added ' + str(i) + ' shorter letter sets.')

    best_score = 0
    best_span = None
    best_centre_letter = None
    best_span_list = None
    new_high_score = False

    for i, this_honeycomb in enumerate(possible_honeycombs, start=1):
        if 's' in this_honeycomb:
            continue
        for this_letter in this_honeycomb:
            honeycomb_score = 0
            centre_letter = this_letter
            span_list = list()
            for this_letter_span in letter_spans:
                if centre_letter in this_letter_span:
                    all_used_letters_in_span = True
                    for this_used_letter in this_letter_span:
                        if this_used_letter not in this_honeycomb:
                            all_used_letters_in_span = False
                            break
                    if all_used_letters_in_span:
                        honeycomb_score += letter_spans[this_letter_span][0]
                        span_list.append(letter_spans[this_letter_span])
            if honeycomb_score > best_score:
                new_high_score = True
                best_score = honeycomb_score
                best_span = this_honeycomb
                best_centre_letter = centre_letter
                best_span_list = span_list

        if new_high_score:
            new_high_score = False
            print('')
            print('After checking ' + str(i) + ' / ' + str(total_honeycombs_to_check) + ' combinations:')
            print('Highest score = ' + str(best_score))
            print('From combination ', end = '')
            for x in best_span:
                print(x, end='')
            print(', centre letter = ' + best_centre_letter)

    print('')
    print('')
    print('FINAL RESULT:')
    print('Highest score = ' + str(best_score))
    print('From combination ', end='')
    for x in best_span:
        print(x, end='')
    print(', centre letter = ' + best_centre_letter)
    for span_list in best_span_list:
        print(span_list)


if __name__ == "__main__":
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    duration = end - start
    print(str(duration.total_seconds()) + " seconds")
