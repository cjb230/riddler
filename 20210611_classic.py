import requests
import pandas as pd
import copy
from itertools import combinations
from math import comb

BORDER_PAGE_URL = 'http://users.econ.umn.edu/~holmes/data/BORDLIST.html'
STATE_AREAS = {'AL': 52420, 'AK': 665384, 'AZ': 113990, 'AR': 53179, 'CA': 163695, 'CO': 104094, 'CT': 5543, 'DE': 2489,
               'DC': 68, 'FL': 65758, 'GA': 59425, 'HI': 10932, 'ID': 83569, 'IL': 57914, 'IN': 36420, 'IA': 56273,
               'KS': 82278, 'KY': 40408, 'LA': 52378, 'ME': 35380, 'MD': 12406, 'MA': 10554, 'MI': 96714, 'MN': 86936,
               'MS': 48432, 'MO': 69707, 'MT': 147040, 'NE': 77348, 'NV': 110572, 'NH': 9349, 'NJ': 8723, 'NM': 121590,
               'NY': 54555, 'NC': 53819, 'ND': 70698, 'OH': 44826, 'OK': 69899, 'OR': 98379, 'PA': 46054, 'RI': 1545,
               'SC': 32020, 'SD': 77116, 'TN': 42144, 'TX': 268596, 'UT': 84897, 'VT': 9616, 'VA': 42775, 'WA': 71298,
               'WV': 24230, 'WI': 65496, 'WY': 97813, 'UM': 16377, 'LM': 80337}
TOTAL_48_AREA = sum(STATE_AREAS.values())


def get_state_sizes():
    my_state_areas = copy.deepcopy(STATE_AREAS)
    my_state_areas.pop('MI')
    my_state_areas.pop('HI')
    my_state_areas.pop('AK')
    my_state_areas.pop('DC')
    return my_state_areas


def get_state_borders(include_point_borders=False, two_michigans=True):
    border_content = requests.get(BORDER_PAGE_URL).content
    df_list = pd.read_html(border_content)
    df = df_list[-1]
    df.drop(columns=[0, 2], inplace=True)
    df.drop([0], inplace=True)
    state_borders = {}
    for row in df.itertuples():
        state_1 = row[1][0:2]
        state_2 = row[1][3:5]
        if state_1 in state_borders:
            state_borders[state_1].add(state_2)
        else:
            state_borders[state_1] = {state_2}

        if state_2 in state_borders:
            state_borders[state_2].add(state_1)
        else:
            state_borders[state_2] = {state_1}
    if not include_point_borders:
        state_borders['AZ'].remove('CO')
        state_borders['CO'].remove('AZ')
        state_borders['NM'].remove('UT')
        state_borders['UT'].remove('NM')
    if two_michigans:
        state_borders.pop('MI')
        state_borders['UM'] = {'WI'}
        state_borders['LM'] = {'IN', 'OH'}
        state_borders['WI'].remove('MI')
        state_borders['WI'].add('UM')
        state_borders['IN'].remove('MI')
        state_borders['IN'].add('LM')
        state_borders['OH'].remove('MI')
        state_borders['OH'].add('LM')
    return state_borders


def get_contiguous_subgroup(node_group, all_edges):
    contiguous_group = {node_group[0], }
    old_group_size = 1
    relevant_borders = all_edges[node_group[0]].intersection(node_group)
    contiguous_group |= relevant_borders
    new_group_size = len(contiguous_group)
    while new_group_size > old_group_size:  # at least one node was added last time through
        all_borders = set()
        for this_node in contiguous_group:
            all_borders |= all_edges[this_node]
        relevant_borders = all_borders.intersection(node_group)
        contiguous_group = relevant_borders
        old_group_size = new_group_size
        new_group_size = len(relevant_borders)
    return contiguous_group


def get_partition_score(partition_dict, nth_smallest=2):
    for this_subpartition in partition_dict:
        this_subpartition_area = 0
        for this_state in this_subpartition:
            this_subpartition_area += STATE_AREAS[this_state]
        partition_dict[this_subpartition] = this_subpartition_area
    ordered_sizes = sorted(partition_dict.values())
    return ordered_sizes[0]


def is_group_contiguous(node_group, all_edges):
    node_group_size = len(node_group)
    if node_group_size == 1:
        return True
    if node_group_size == 2:
        if node_group[0] in all_edges.keys():  # relies on the dictionary of edges containing both directions
            if node_group[1] in all_edges[node_group[0]]:
                return True
        return False
    if node_group_size > 2:
        if node_group_size == len(get_contiguous_subgroup(node_group, all_edges)):
            return True
        else:
            return False


def group_area(state_group):
    return sum({STATE_AREAS[state] for state in state_group})


def min_state_group_size(states):
    answer = 0
    ordered_sizes = sorted(get_state_sizes().values())
    for i in range(0, states):
        answer += ordered_sizes[i]
    return answer


def main():
    state_sizes = get_state_sizes()
    print("State sizes loaded")
    state_set = set(state_sizes.keys())
    state_borders = get_state_borders()
    print("State borders loaded")
    print('Lower 48 area (square miles) = ', TOTAL_48_AREA)
    best_score = 0
    for this_state_number in range(1, len(state_sizes)):
        min_size = min_state_group_size(this_state_number)
        max_possible_score = (TOTAL_48_AREA - min_size) / 2
        possible_combs = comb(49, this_state_number)
        print()
        print(this_state_number, ' state(s) at a time')
        print(possible_combs, ' possible groups with', this_state_number, 'states')
        print('best score so far =', best_score)
        print('max possible score with this many states = ', max_possible_score)
        if max_possible_score < best_score:
            print('Too many states, nothing better is possible')
            exit()

        for this_group in combinations(state_sizes, this_state_number):
            if is_group_contiguous(this_group, state_borders):
                max_possible_score = (TOTAL_48_AREA - group_area(this_group)) / 2
                if max_possible_score > best_score:
                    contiguous_subgroups = dict()
                    remaining_state_tuple = tuple(state_set.difference(this_group))
                    next_subgroup = get_contiguous_subgroup(remaining_state_tuple, state_borders)
                    contiguous_subgroups[tuple(next_subgroup)] = 0
                    while len(next_subgroup) < len(remaining_state_tuple):
                        remaining_state_tuple = tuple(set(remaining_state_tuple).difference(next_subgroup))
                        next_subgroup = get_contiguous_subgroup(remaining_state_tuple, state_borders)
                        contiguous_subgroups[tuple(next_subgroup)] = 0
                    if len(contiguous_subgroups) == 2:
                        new_score = get_partition_score(contiguous_subgroups)
                        if new_score > best_score:
                            best_score = new_score
                            print()
                            print('new best')
                            print('score = ', best_score)
                            print('group =', str(this_group))
                            for subgroup in contiguous_subgroups:
                                print('  ', str(subgroup))


if __name__ == '__main__':
    main()
