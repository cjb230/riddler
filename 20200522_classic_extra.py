import datetime
import requests

DICTIONARY_FILE_URL = 'https://norvig.com/ngrams/word.list'
ALL_STATE_NAMES = {'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
                   'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
                   'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
                   'Kentucky', 'Louisiana', 'Maine', 'Maryland',
                   'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
                   'Missouri', 'Montana', 'Nebraska', 'Nevada',
                   'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
                   'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
                   'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
                   'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
                   'Virginia', 'Washington', 'West Virginia', 'Wisconsin',
                   'Wyoming'}
PREPARED_STATE_NAMES = dict()


def get_dictionary_file():
    relevant_words = requests.get(DICTIONARY_FILE_URL).content
    return relevant_words


def prepare_state_names():
    global PREPARED_STATE_NAMES
    for this_state in ALL_STATE_NAMES:
        str = ''
        this_prepared_state_name = str.join(sorted(set(this_state.lower().replace(' ', ''))))
        if this_prepared_state_name in PREPARED_STATE_NAMES:
            PREPARED_STATE_NAMES[this_prepared_state_name].append(this_state)
        else:
            PREPARED_STATE_NAMES[this_prepared_state_name] = [this_state]


def have_common_letters(prepared_string_1, prepared_string_2):
    common_letter_found = False
    str_1_len = len(prepared_string_1)
    str_2_len = len(prepared_string_2)
    str_1_comparison_index = 0
    str_2_comparison_index = 0
    while str_1_comparison_index < str_1_len and str_2_comparison_index < str_2_len:
        str_1_char = prepared_string_1[str_1_comparison_index]
        str_2_char = prepared_string_2[str_2_comparison_index]
        if str_1_char == str_2_char:
            common_letter_found = True
            break
        elif ord(str_1_char) > ord(str_2_char):
            str_2_comparison_index += 1
        else:
            str_1_comparison_index += 1

    return common_letter_found


def is_mackerel(test_word):
    result = False
    common_letter_states = 0
    no_common_letter_states = 0
    no_common_letter_first_state = ''
    str = ''
    prepared_test_word = str.join(sorted(set(test_word.lower().replace(' ', ''))))
    for prepared_state_name in PREPARED_STATE_NAMES.keys():
        if have_common_letters(prepared_test_word, prepared_state_name):
            common_letter_states += 1
        else:
            no_common_letter_states += 1
            if no_common_letter_states == 1:
                no_common_letter_first_state = PREPARED_STATE_NAMES[prepared_state_name][0]
            else:
                break

    if no_common_letter_states == 1 and common_letter_states == 49:
        result = no_common_letter_first_state
    return result


def main(dictionary_file):
    prepare_state_names()
    all_words = [this_line for this_line in dictionary_file.decode("utf-8").splitlines()]

    state_mackerels = dict()
    for this_word in all_words:
        this_result = is_mackerel(this_word)
        if this_result:
            if this_result in state_mackerels:
                state_mackerels[this_result] = state_mackerels[this_result] + 1
            else:
                state_mackerels[this_result] = 1
    print(sorted(state_mackerels.items(), key=lambda x:x[1], reverse=True)[0])


if __name__ == "__main__":
    download_start = datetime.datetime.now()
    dictionary_file = get_dictionary_file()
    download_end = datetime.datetime.now()
    download_duration = download_end - download_start
    print('Download took ' + str(download_duration.total_seconds()) + " seconds")
    processing_start = datetime.datetime.now()
    main(dictionary_file)
    processing_end = datetime.datetime.now()
    processing_duration = processing_end - processing_start
    print('Processing took ' + str(processing_duration.total_seconds()) + " seconds")
