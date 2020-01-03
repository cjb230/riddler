SOURCE_FILE = '20200103_input_enable1.txt'


def letter_set(word):
    return {char for char in word}


def get_possible_pangrams():
    with open(SOURCE_FILE) as f:
        possible_pangrams = [{char for char in this_line} for this_line in f.read().splitlines() if len({char for char in this_line}) == 7]
    return possible_pangrams


def get_relevant_word_list():
    with open(SOURCE_FILE) as f:
        relevant_words = [this_line for this_line in f.read().splitlines() if len(this_line) > 4 and len({char for char in this_line}) < 8]
    return relevant_words


def word_score(word):
    if len(word == 4):
        return 1
    elif len(word) < 4:
        print('SHORT WORD ISSUE: ' + word)
    elif len(letter_set(word)) == 7:
        return 7 + len(word)
    else:
        return len(word)


def main():
    relevant_words = get_relevant_word_list()
    print(str(len(relevant_words)) + ' relevant words')
    possible_pangrams = get_possible_pangrams()
    print(str(len(possible_pangrams)) + ' words with 7-letter spans')

    word_by_letter_span = dict()
    i = 0
    for this_word in relevant_words:
        i += 1
        this_word_letters = letter_set(this_word)
        if this_word_letters in word_by_letter_span.keys():
            word_by_letter_span[this_word_letters][0] += word_score(this_word)
            word_by_letter_span[this_word_letters][1].append(this_word)
        else:
            word_by_letter_span[this_word_letters] = [0, [this_word]]

    print(len(this_word_letters))


if __name__ == "__main__":
    main()
    get_possible_pangrams()
    #relevant_word_list()