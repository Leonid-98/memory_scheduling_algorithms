import itertools
from operator import itemgetter
from tkinter import *


class MyGui(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.width = 1001
        master.title("Protsessoriaja haldus")
        master.geometry(f"{self.width + 40}x{370}")
        master.resizable(False, False)
        self.font = ("Bahnschrift SemiBold", 12)
        self.colors = {
            "P1": "#0CF799",
            "P2": "#4B43EB",
            "P3": "#EB008E",
            "P4": "#D4750B",
            "P5": "#D8F50F",
            "P6": "#0CF716",
            "P7": "#0B86D4",
            "P8": "#A000EB",
            "P9": "#D43C0B",
            "P10": "#F5D00F",
        }
        defaults_for_option_menu = [
            "Enda oma üleval",
            "0,7;1,5;2,3;3,1;4,2;5,1",
            "0,2;1,4;12,4;15,5;21,10",
            "0,4;1,5;2,2;3,1;4,6;6,3",
        ]
        self.option_menu_choise = defaults_for_option_menu[0]

        self.outercanvas = Canvas(master, bg="#dbf7ff", width=self.width + 40, height=370)
        self.outercanvas.pack()

        self.innercanvas = Canvas(self.outercanvas, width=self.width, height=201, bg="#7b9ba4", highlightthickness=0)
        self.outercanvas.create_window(20, 20, anchor=NW, window=self.innercanvas)

        first_fit_button = Button(self.outercanvas, text="first-fit", font=self.font, command=lambda: self.calculate_schedue_and_draw("first-fit"))
        self.outercanvas.create_window(20, 240, anchor=NW, height=30, width=80, window=first_fit_button)

        last_fit_btn = Button(self.outercanvas, text="last-fit", font=self.font, command=lambda: self.calculate_schedue_and_draw("last-fit"))
        self.outercanvas.create_window(120, 240, anchor=NW, height=30, width=80, window=last_fit_btn)

        best_fit_btn = Button(self.outercanvas, text="best-fit", font=self.font, command=lambda: self.calculate_schedue_and_draw("best-fit"))
        self.outercanvas.create_window(220, 240, anchor=NW, height=30, width=80, window=best_fit_btn)

        worst_fit_btn = Button(self.outercanvas, text="worst-fit", font=self.font, command=lambda: self.calculate_schedue_and_draw("worst-fit"))
        self.outercanvas.create_window(320, 240, anchor=NW, height=30, width=80, window=worst_fit_btn)

        rand_fit_btn = Button(self.outercanvas, text="rand-fit", font=self.font, command=lambda: self.calculate_schedue_and_draw("worst-fit"))
        self.outercanvas.create_window(420, 240, anchor=NW, height=30, width=80, window=rand_fit_btn)

        clear_btn = Button(self.outercanvas, text="Reset", font=self.font, command=lambda: self.reset_inner_canvas())
        self.outercanvas.create_window(520, 240, anchor=NW, height=30, width=80, window=clear_btn)

        self.entry = Entry(self.outercanvas, font=self.font, state=NORMAL)
        self.entry.insert(END, "1,10;3,3;4,1;8,6;15,2")
        self.outercanvas.create_window(20, 280, anchor=NW, height=30, width=220, window=self.entry)

        self.option_menu_var = StringVar()
        self.option_menu_var.set(defaults_for_option_menu[0])
        self.option_menu = OptionMenu(
            self.outercanvas, self.option_menu_var, *defaults_for_option_menu, command=lambda event_choice: self.check_option_menu_choise(event_choice)
        )
        self.option_menu.config(font=self.font)
        menu = master.nametowidget(self.option_menu.menuname)
        menu.config(font=self.font)
        self.outercanvas.create_window(20, 320, anchor=NW, height=30, width=220, window=self.option_menu)

        self.name_label = Label(self.outercanvas, text="A: [3, 5], B: [1, 2]", font=self.font, bg="#dbf7ff")
        self.outercanvas.create_window(630, 240, anchor=NW, height=50, width=300, window=self.name_label)

    def convert_string_to_order(self, string):
        """abifunktsioon mis teisendab sisend kujuks: str "1,0;2,3" --> list [[1, 0], [2, 3]] ning kohe sorrteerib saabumise aja kaudu"""
        return sorted([[int(time) for time in process.split(",")] for process in string.split(";")], key=itemgetter(0))

    def reset_inner_canvas(self):
        pass
        """event funktsion, puhastab sisemine canvas"""
        self.innercanvas.delete("all")
        self.entry.delete(0, END)
        self.entry.insert(END, "1,10;3,3;4,1;8,6;15,2")

    def check_option_menu_choise(self, event_choice):
        """event funktsion option menu jaoks"""
        self.option_menu_choise = event_choice
        if event_choice == "Enda oma üleval":
            self.entry.config(state=NORMAL)
        else:
            self.entry.config(state=DISABLED)

    def calculate_schedue_and_draw(self, algorithm: str):
        self.draw_process_on_canvas()

    def get_coordinates(self, row, column):
        """Abifunktsioon, mis tagastab Rectangle Objekti coordinatid et neeed joonistada"""
        return (column * 20, row * 20, (column + 1) * 20, row * 20 + 20)

    def draw_process_on_canvas(self):
        """event põhifunktsioon arvutamise jaoks"""
        count = 0
        for row in range(10):
            for column in range(50):
                x1, y1, x2, y2 = self.get_coordinates(row, column)
                color = "#7b9ba4"
                self.innercanvas.create_rectangle(x1, y1, x2, y2, fill=color)
                # self.innercanvas.create_text((x1 + 10), (y1 + 10), text="B", font=self.font)

if __name__ == "__main__":
    root = Tk()
    my_gui = MyGui(root)
    my_gui.mainloop()
