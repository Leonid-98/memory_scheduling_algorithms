import itertools
from operator import itemgetter
from tkinter import *
from memory_algorithm import *


class MyGui(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.width = 1001
        self.inner_height = 201
        master.title("Protsessoriaja haldus")
        master.geometry(f"{self.width + 40}x{370}")
        master.resizable(False, False)
        self.font = ("Bahnschrift SemiBold", 12)
        self.colors = {
            "A": "#0CF799",
            "B": "#4B43EB",
            "C": "#EB008E",
            "D": "#D4750B",
            "E": "#D8F50F",
            "F": "#0CF716",
            "G": "#0B86D4",
            "H": "#A000EB",
            "I": "#D43C0B",
            "J": "#F5D00F",
            EMPTY_CELL: "#7b9ba4",
            ERROR_CELL: "#1c1c1c",
        }
        defaults_for_option_menu = [
            "Enda oma üleval",
            "4,5;2,7;9,2;4,6;7,1;6,4;8,8;3,6;1,10;9,2",
            "1,10;6,6;3,9;2,4;1,6;5,2;1,4;5,2;2,1;2,7",
            "5,10;6,6;3,9;8,4;3,6;5,12;1,4;15,3;3,4;9,7",
        ]
        self.option_menu_choise = defaults_for_option_menu[0]

        self.outercanvas = Canvas(master, bg="#dbf7ff", width=self.width + 40, height=370)
        self.outercanvas.pack()

        self.innercanvas = Canvas(self.outercanvas, width=self.width, height=self.inner_height, bg="#7b9ba4", highlightthickness=0)
        self.outercanvas.create_window(20, 20, anchor=NW, window=self.innercanvas)

        first_fit_button = Button(self.outercanvas, text="first-fit", font=self.font, command=lambda: self.calculate_schedue_and_draw(FIRST_FIT))
        self.outercanvas.create_window(20, 240, anchor=NW, height=30, width=80, window=first_fit_button)

        last_fit_btn = Button(self.outercanvas, text="last-fit", font=self.font, command=lambda: self.calculate_schedue_and_draw(LAST_FIT))
        self.outercanvas.create_window(120, 240, anchor=NW, height=30, width=80, window=last_fit_btn)

        best_fit_btn = Button(self.outercanvas, text="best-fit", font=self.font, command=lambda: self.calculate_schedue_and_draw(BEST_FIT))
        self.outercanvas.create_window(220, 240, anchor=NW, height=30, width=80, window=best_fit_btn)

        worst_fit_btn = Button(self.outercanvas, text="worst-fit", font=self.font, command=lambda: self.calculate_schedue_and_draw(WORST_FIT))
        self.outercanvas.create_window(320, 240, anchor=NW, height=30, width=80, window=worst_fit_btn)

        rand_fit_btn = Button(self.outercanvas, text="rand-fit", font=self.font, command=lambda: self.calculate_schedue_and_draw(RAND_FIT))
        self.outercanvas.create_window(420, 240, anchor=NW, height=30, width=80, window=rand_fit_btn)

        clear_btn = Button(self.outercanvas, text="Reset", font=self.font, command=lambda: self.reset_inner_canvas())
        self.outercanvas.create_window(520, 240, anchor=NW, height=30, width=80, window=clear_btn)

        self.entry = Entry(self.outercanvas, font=self.font, state=NORMAL)
        self.entry.insert(END, "1,8;35,4;3,6;4,2;1,4;3,3;1,2;5,1;50,1")
        self.outercanvas.create_window(20, 280, anchor=NW, height=30, width=290, window=self.entry)

        self.option_menu_var = StringVar()
        self.option_menu_var.set(defaults_for_option_menu[0])
        self.option_menu = OptionMenu(
            self.outercanvas, self.option_menu_var, *defaults_for_option_menu, command=lambda event_choice: self.check_option_menu_choise(event_choice)
        )
        self.option_menu.config(font=self.font)
        menu = master.nametowidget(self.option_menu.menuname)
        menu.config(font=self.font)
        self.outercanvas.create_window(20, 320, anchor=NW, height=30, width=290, window=self.option_menu)

        self.name_label = Label(self.outercanvas, text="zxc 123", font=self.font, bg="#dbf7ff")
        self.outercanvas.create_window(630, 240, anchor=NW, height=50, width=300, window=self.name_label)

        self.max_steps = 10 # to be updated

    def convert_string_to_order(self, string) -> list:
        """abifunktsioon mis teisendab sisend kujuks: str "1,0;2,3" --> list [[1, 0], [2, 3]]"""
        return [[int(time) for time in process.split(",")] for process in string.split(";")]

    def reset_inner_canvas(self):
        """event funktsion, puhastab sisemine canvas"""
        self.innercanvas.delete("all")
        self.entry.delete(0, END)
        self.entry.insert(END, "1,8;35,4;3,6;4,2;1,4;3,3;1,2;5,1;50,1")

    def check_option_menu_choise(self, event_choice):
        """event funktsion option menu jaoks"""
        self.option_menu_choise = event_choice
        if event_choice == "Enda oma üleval":
            self.entry.config(state=NORMAL)
        else:
            self.entry.config(state=DISABLED)

    def calculate_schedue_and_draw(self, type_of_algorithm):
        """event põhifunktsioon kalkuleerimise jaoks"""
        self.innercanvas.delete("all")
        if self.option_menu_choise == "Enda oma üleval":
            order = self.convert_string_to_order(self.entry.get())
        else:
            order = self.convert_string_to_order(self.option_menu_choise)
        
        algorithm = MemoryAlgorithm(order)
        self.max_steps = algorithm.get_max_steps(order)
        memory = algorithm.get_filled_memory(type_of_algorithm)
        self.draw_process_on_canvas(memory)

    def get_coordinates(self, row, column):
        """Abifunktsioon, mis tagastab Rectangle Objekti coordinatid et neeed joonistada"""
        div = int(round(self.inner_height/self.max_steps)) - 1
        return (column * 20, row * div, (column + 1) * 20, row * div + div)

    def draw_process_on_canvas(self, memory):
        """event abifunktsioon, et joonistada maatriks"""
        for row in range(self.max_steps):
            for column in range(MAX_SIZE):
                x1, y1, x2, y2 = self.get_coordinates(row, column)
                process_name = memory[row][column]
                color = self.colors[process_name]
                self.innercanvas.create_rectangle(x1, y1, x2, y2, fill=color)
                self.innercanvas.create_text((x1 + 10), (y1 + 10), text=process_name, font=self.font)


if __name__ == "__main__":
    root = Tk()
    my_gui = MyGui(root)
    my_gui.mainloop()
