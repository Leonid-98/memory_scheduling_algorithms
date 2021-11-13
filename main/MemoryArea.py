from operator import itemgetter
from itertools import groupby
import string

MAX_PROCESSES = 10
PROCESS_NAMES = list(string.ascii_uppercase[:MAX_PROCESSES])
EMPTY_CELL = "X"
MAX_STEPS = 10
MAX_SIZE = 50


#
TEXT_INPUT = "1,8;35,4;3,6;4,2;1,4;3,3;1,2;5,1;50,1"
def convert_string_to_order(string) -> list:
    """abifunktsioon mis teisendab sisend kujuks: str "1,0;2,3" --> list [[1, 0], [2, 3]]"""
    return [[int(time) for time in process.split(",")] for process in string.split(";")]
order = convert_string_to_order(TEXT_INPUT)
#


    
def generate_empty_memory_space():
    memory_space = []
    for _ in range(MAX_STEPS):
        one_line = []
        for _ in range(MAX_SIZE):
            one_line.append(EMPTY_CELL)
        memory_space.append(one_line)

    return memory_space

def check_for_free_sectors(row: list) -> list:
    """Kontrollib, kas vaadeldavas reas on vaba ruumi, jagub seektoriks"""
    free_indexes = []
    for i in range(len(row)):
        if row[i] == EMPTY_CELL:
            free_indexes.append(i)
    
    # [1, 2, 4, 5, 7] -> [1, 2], [4, 5], [7]
    free_sectors = []
    for _, g in groupby(enumerate(free_indexes), lambda x: x[0] - x[1]):
        free_sectors.append(list(map(itemgetter(1), g)))

    return free_sectors

def check_if_process_fits(free_sectors: list, process_size: int) -> list:
    available_sectors = []
    for i in range(len(free_sectors)):
        if len(free_sectors[i]) >= process_size:
            available_sectors.append(i)
    return available_sectors

memory_space = generate_empty_memory_space()


def allocate_prrocessees(memory, order):
    for index_of_process, process in enumerate(order):
        process_name = PROCESS_NAMES.pop(0)
        width = process[0]
        height = process[1]

        # fill the first row
        current_line = memory[index_of_process]
        free_areas = check_for_free_sectors(current_line)
        avaiable_areas = check_if_process_fits(free_areas, width)
        is_process_allocated = True if avaiable_areas else False
        
        if is_process_allocated:
            # first-fit
            sector = free_areas[avaiable_areas[0]]
            start = sector[0]
            end = sector[0] + width - 1
            for j in range(height):
                for l in range(start, end + 1):
                    memory[index_of_process + j][l] = process_name



    return memory


memory = allocate_prrocessees(memory_space, order)
for i in memory:
    print(i)

print(check_for_free_sectors(memory[6]))



