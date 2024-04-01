import tkinter
from tkinter.colorchooser import askcolor
from typing import TextIO

class TermColors:
    INITIAL_COLOR = "#FFFFFF"

    def __init__(self, path: str) -> None:
        self.path = path
        self.root = tkinter.Tk()
        self.chose_color = TermColors.INITIAL_COLOR
        self.color_name = tkinter.StringVar(self.root, "very white")

        self.canvas = self.terminal_inspired_canvas()
        self.create_example_text()
        self.canvas.pack()
        self.save_color_button().pack(side="bottom")
        tkinter.Button(self.root, text="pick", command=self.pick_color).pack(side="bottom")
        self.color_name_field().pack(side="bottom")

    def terminal_inspired_canvas(self) -> tkinter.Canvas:
        c = tkinter.Canvas(self.root, width=320, height=200, bg="black")
        c.bind("1", self.pick_color)
        return c

    def create_example_text(self) -> None:
        self.canvas.create_text(130, 20, text="python -m badCooker init", fill=self.chose_color, font=("ubuntu 24", 20))

    def save_color_button(self) -> tkinter.Button:
        return tkinter.Button(self.root, text="save ->", fg="blue", command=self.save_color)

    def color_name_field(self) -> tkinter.Entry:
        return tkinter.Entry(self.root, textvariable=self.color_name)

    def pick_color(self) -> None:
        colors = askcolor(parent=self.root, initialcolor=TermColors.INITIAL_COLOR)
        hex_color = colors[1]
        self.chose_color = hex_color
        self.create_example_text()

    def save_color(self) -> None:
        with open(self.path, "a") as f:
            self.write_color(f)

    def write_color(self, file: TextIO) -> None:
        color_name = "_".join(self.color_name.get().split()).upper()
        item = f"{color_name},{self.chose_color},"
        file.write(item)

    def __call__(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    colors_tool = TermColors(path="/Users/andrewrudenko/PycharmProjects/badCook/resources/term_colors.csv")
    colors_tool()
