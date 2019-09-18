ALL_ABBREVS = {'AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL',
               'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
               'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX',
               'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY'}


def recurse(trial_string, remaining_abbrevs):
    trial_string_len = len(trial_string)
    return_set = set()

    for abbrev in remaining_abbrevs:
        if abbrev[0] == trial_string[-1]:
            shorter_abbrevs = remaining_abbrevs.copy()
            shorter_abbrevs.remove(abbrev)
            return_set = return_set.union(recurse(trial_string + abbrev[-1], shorter_abbrevs))

    if len(return_set) > 0:
        return sift_set(return_set)
    else:
        return_set.add(trial_string)
        return return_set


def main():
    states_done = 1
    overall_longest = set()
    for abbrev in ALL_ABBREVS:
        longest_state_strings = set()
        print("Starting state " + str(states_done) + ", " + abbrev)
        remaining_set = ALL_ABBREVS.copy()
        remaining_set.remove(abbrev)
        longest_state_strings = recurse(abbrev, remaining_set)
        example_longest = list(longest_state_strings)[0]
        print("Max length for " + abbrev + " = " + str(len(example_longest)) + " e.g. " + example_longest)
        overall_longest = overall_longest.union(longest_state_strings)
        states_done += 1
    overall_longest = sift_set(overall_longest)
    print(overall_longest)


def sift_set(full_set):
    longest_string_length = 0
    return_set = set()
    for states_string in full_set:
        if len(states_string) > longest_string_length:
            longest_string_length = len(states_string)
    for states_string in full_set:
        if len(states_string) == longest_string_length:
            return_set.add(states_string)
    return return_set


if __name__ == '__main__':
    main()
