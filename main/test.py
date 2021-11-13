from operator import itemgetter
from itertools import groupby

seq1 = list("AXXXXXAXXXXXXXXAXXXXXXXXXXXXXXXXXXXXXXXXAXXXXXXXXX")
seq2 = list("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
CURRENT_SEQ = seq1

def get_free_memory_sectors(row: list) -> list:
    free_space_indexes = []
    for i in range(len(CURRENT_SEQ)):
        if CURRENT_SEQ[i] == "X":
            free_space_indexes.append(i)

    free_space_groups = []
    for k, g in groupby(enumerate(free_space_indexes), lambda x: x[0]-x[1]):
        free_space_groups.append(list(map(itemgetter(1), g)))

    return free_space_groups

print(get_free_memory_sectors(CURRENT_SEQ))


