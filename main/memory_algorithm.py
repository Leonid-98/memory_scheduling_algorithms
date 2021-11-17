from random import randint
import random
import string
from itertools import groupby
from operator import itemgetter
from tkinter.constants import PIESLICE

EMPTY_CELL = ""
ERROR_CELL = "-"
MAX_SIZE = 50

FIRST_FIT = "ff"
LAST_FIT = "lf"
BEST_FIT = "bf"
WORST_FIT = "wf"
RAND_FIT = "rf"


class MemoryAlgorithm:
    def __init__(self, order):
        self.order = order
        self.max_steps = self.get_max_steps(order)
        self.process_names = list(string.ascii_uppercase[: self.max_steps])
        self.not_fitted_name = None

    def get_not_fitted_name(self):
        return self.not_fitted_name

    def get_max_steps(self, order):
        max_value = 0
        for i, value in enumerate(order):
            if value[1] + i > max_value:
                max_value = value[1] + i
        return max_value

    def _generate_empty_memory_space(self):
        """Genereerib vaba ruumi (maatriks) suurusega 10x50"""
        memory_space = []
        for _ in range(self.max_steps):
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
            free_areas = self._check_for_free_sectors(current_line)  # list of list = list of free seectors
            avaiable_areas_indexes = self._check_if_process_fits(free_areas, width)  # list of index = list on number of AVAILABLE sector
            is_process_allocated = True if avaiable_areas_indexes else False

            if type_of_algorithm == FIRST_FIT:
                i = 0

            elif type_of_algorithm == LAST_FIT:
                i = -1

            elif type_of_algorithm == BEST_FIT:
                best_fit = 999
                best_fit_index = -1
                for i, value in enumerate(avaiable_areas_indexes):
                    dif = len(free_areas[value]) - width
                    if dif < best_fit and dif >= 0:
                        best_fit = dif
                        best_fit_index = i
                i = best_fit_index

            elif type_of_algorithm == WORST_FIT:
                free_areas = sorted(free_areas, key=len)
                avaiable_areas_indexes = self._check_if_process_fits(free_areas, width)
                i = -1

            elif type_of_algorithm == RAND_FIT:
                avaiable_areas_indexes = [i for i in range(len(free_areas))]
                i = random.choice(avaiable_areas_indexes)
                if width > len(free_areas[i]):
                    is_process_allocated = False

            if is_process_allocated:
                index_of_area = avaiable_areas_indexes[i]
                sector = free_areas[index_of_area]
                self._put_process_in_memory(sector, width, height, index_of_process, process_name, memory)
            else:
                self.not_fitted_name = process_name
                for i in range(len(current_line)):
                    if current_line[i] == EMPTY_CELL:
                        current_line[i] = ERROR_CELL
                break

        return memory


if __name__ == "__main__":
    # 1,8;7,4;10,6;25,2;1,4;13,3;6,2;8,1;50,1
    order = [[1, 8], [7, 4], [10, 6], [25, 2], [1, 4], [13, 3], [6, 2], [8, 1], [50, 1], [50, 1]]
    algorithm = MemoryAlgorithm(order)
    memory = algorithm.get_filled_memory(BEST_FIT)
    # for i in memory:
    #     print(i)
