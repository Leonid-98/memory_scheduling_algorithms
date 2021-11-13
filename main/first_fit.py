import string

MAX_PROCESSES = 10
PROCESS_NAMES = list(string.ascii_uppercase[:MAX_PROCESSES])
TEXT_INPUT = "1,8;35,4;3,6;4,2;1,4;3,3;1,2;5,1;50,1"
EMPTY_CELL = "X"
memory = []


def convert_string_to_order(string) -> list:
    """abifunktsioon mis teisendab sisend kujuks: str "1,0;2,3" --> list [[1, 0], [2, 3]]"""
    return [[int(time) for time in process.split(",")] for process in string.split(";")]


for row in range(10):
    one_line = []
    for column in range(50):
        one_line.append(EMPTY_CELL)
    memory.append(one_line)

for i in memory:
    print(i)


order = convert_string_to_order(TEXT_INPUT)
print(order)


def allocate_prrocessees(memory, order):
    for index_of_process, process in enumerate(order):
        process_name = PROCESS_NAMES.pop(0)
        width = process[0]
        height = process[1]

        # fill the first row
        free_space_count = 0
        is_process_were_allocated = False
        current_line = memory[index_of_process]
        for i in range(len(current_line)):
            if current_line[i] == EMPTY_CELL:
                free_space_count += 1
            if width == free_space_count:
                is_process_were_allocated = True
                break

        if is_process_were_allocated:
            start = i - width + 1 
            end = i
            # fill the column
            for j in range(height):
                for l in range(start, end + 1):
                    memory[index_of_process + j][l] = process_name
    return memory


memory = allocate_prrocessees(memory, order)
for i in memory:
    print(i)
