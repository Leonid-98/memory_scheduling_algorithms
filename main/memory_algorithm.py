import random
import string
from itertools import groupby
from operator import itemgetter

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

        # [1, 2, 4, 5, 7] -> [1, 2], [4, 5], [7] ehk sektoriks jagumine
        free_sectors = []
        for _, g in groupby(enumerate(free_indexes), lambda x: x[0] - x[1]):
            free_sectors.append(list(map(itemgetter(1), g)))

        return free_sectors

    def _check_if_process_fits(self, free_sectors, process_size) -> list:
        """Kontrollib, kas protsess mahub vaba sektorisse, tagastab vaba sektori indeksid"""
        available_sector_indexes = []
        for i in range(len(free_sectors)):
            if len(free_sectors[i]) >= process_size:
                available_sector_indexes.append(i)
        return available_sector_indexes

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

            current_line = memory[index_of_process]
            free_sectors = self._check_for_free_sectors(current_line)                  # list of list = list of free seectors
            avaiable_sector_indexes = self._check_if_process_fits(free_sectors, width)  # list of indexes = list on number of AVAILABLE sector
            is_process_allocated = True if avaiable_sector_indexes else False

            # valin, mis sektor kasutan. i on sektri indeks
            if type_of_algorithm == FIRST_FIT:
                i = 0

            elif type_of_algorithm == LAST_FIT:
                i = -1

            elif type_of_algorithm == BEST_FIT:
                best_fit = 999
                best_fit_index = -1
                for i, value in enumerate(avaiable_sector_indexes):
                    dif = len(free_sectors[value]) - width
                    if dif < best_fit and dif >= 0:
                        best_fit = dif
                        best_fit_index = i
                i = best_fit_index

            elif type_of_algorithm == WORST_FIT:
                free_sectors = sorted(free_sectors, key=len)
                avaiable_sector_indexes = self._check_if_process_fits(free_sectors, width)
                i = -1

            elif type_of_algorithm == RAND_FIT:
                avaiable_sector_indexes = [i for i in range(len(free_sectors))]
                i = random.choice(avaiable_sector_indexes)
                if width > len(free_sectors[i]):
                    is_process_allocated = False

            # panen protsess sektorisse (või katkestan töö kui ei mahu)
            if is_process_allocated:
                index_of_area = avaiable_sector_indexes[i]
                sector = free_sectors[index_of_area]
                self._put_process_in_memory(sector, width, height, index_of_process, process_name, memory)
            else:
                self.not_fitted_name = process_name
                for i in range(len(current_line)):
                    if current_line[i] == EMPTY_CELL:
                        current_line[i] = ERROR_CELL
                break

        return memory
