from operator import itemgetter
from itertools import groupby
import string

MAX_PROCESSES = 10
PROCESS_NAMES = list(string.ascii_uppercase[:MAX_PROCESSES])
EMPTY_CELL = "X"
MAX_STEPS = 10
MAX_SIZE = 50


class MemoryArea:
    def __init__(self):
        # Maatriks suurusega 10x50
        self.memory_space = self.generate_empty_memory_space()
        
    def generate_empty_memory_space(self):
        memory_space = []
        for _ in range(MAX_STEPS):
            one_line = []
            for _ in range(MAX_SIZE):
                one_line.append(EMPTY_CELL)
            memory_space.append(one_line)

        return memory_space

    def check_for_free_sectors(self, row: list) -> list:
        """Kontrollib, kas vaadeldavas reas on vaba ruumi, jagub seektoriks"""
        free_space_indexes = []
        for i in range(len(row)):
            if row[i] == EMPTY_CELL:
                free_space_indexes.append(i)
        
        # [1, 2, 4, 5, 7] -> [1, 2], [4, 5], [7]
        free_space_groups = []
        for _, g in groupby(enumerate(free_space_indexes), lambda x: x[0] - x[1]):
            free_space_groups.append(list(map(itemgetter(1), g)))

        return free_space_groups

    def put_process_in_memory():
        pass
