import string
from itertools import groupby
from operator import itemgetter

EMPTY_CELL = ""
ERROR_CELL = "-"
MAX_STEPS = 10
MAX_SIZE = 50

FIRST_FIT = "ff"
LAST_FIT = "lf"
BEST_FIT = "bf"
WORST_FIT = "wf"
RAND_FIT = "rf"


class MemoryAlgorithm:
    def __init__(self, order):
        self.order = order
        self.process_names = list(string.ascii_uppercase[:MAX_STEPS])

    def _generate_empty_memory_space(self):
        """Genereerib vaba ruumi (maatriks) suurusega 10x50"""
        memory_space = []
        for _ in range(MAX_STEPS):
            one_line = []
            for _ in range(MAX_SIZE):
                one_line.append(EMPTY_CELL)
            memory_space.append(one_line)

        return memory_space

    def _check_for_free_sectors(self, row) -> list:
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

    def _check_if_process_fits(self, free_sectors, process_size) -> list:
        """Kontrollib, kas protsess mahub vaba sektorisse, tagastab vaba sektori indeksid"""
        available_sectors = []
        for i in range(len(free_sectors)):
            if len(free_sectors[i]) >= process_size:
                available_sectors.append(i)
        return available_sectors

    def _put_process_in_memory(self, sector, width, height, index_of_process, process_name, memory):
        """Paneb mällu (matriksi) protsessid vastavalt vaba sektorile"""
        start = sector[0]
        end = sector[0] + width - 1
        for i in range(height):
            for j in range(start, end + 1):
                memory[index_of_process + i][j] = process_name

    def get_filled_memory(self, type_of_algorithm) -> list:
        """Põhifunktsioon, mis tagastab mälu sisu matriksina"""
        memory = self._generate_empty_memory_space()
        for index_of_process, process in enumerate(self.order):
            process_name = self.process_names.pop(0)
            width = process[0]  # process size
            height = process[1]  # number of steps

            # fill the first row
            current_line = memory[index_of_process]
            free_areas = self._check_for_free_sectors(current_line)
            avaiable_areas = self._check_if_process_fits(free_areas, width)
            is_process_allocated = True if avaiable_areas else False

            if is_process_allocated:
                # first-fit
                sector = free_areas[avaiable_areas[0]]
                self._put_process_in_memory(sector, width, height, index_of_process, process_name, memory)
            else:
                print("proceess can't be allocated")
                for i in range(len(current_line)):
                    if current_line[i] == EMPTY_CELL:
                        current_line[i] = ERROR_CELL
                break

        return memory


if __name__ == "__main__":
    # "1,10;6,6;3,9;2,4;1,6;5,2;1,4;5,2;2,1;2,7"
    order = [[1, 10], [6, 6], [3, 9], [2, 4], [1, 6], [5, 2], [1, 4], [5, 2], [2, 1], [2, 7]]
    algorithm = MemoryAlgorithm(order)
    memory = algorithm.get_filled_memory(FIRST_FIT)
    for i in memory:
        print(i)
