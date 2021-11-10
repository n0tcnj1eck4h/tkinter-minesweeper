#!/usr/bin/env python3.9
import os

from Board import *
from tkinter import *
from tkinter import ttk
from Skin import *


class DifficultyPicker(Toplevel):
    def __init__(self, parent, board, **kwargs):
        super().__init__(parent, **kwargs)
        self.board = board
        self.title("Wybór trudności")
        # Create a Label Text

        self.label1 = Label(self, text="Ilość min:")
        self.label2 = Label(self, text="Szerokość planszy:")
        self.label3 = Label(self, text="Wyskokość planszy:")

        self.entry1 = Entry(self)
        self.entry2 = Entry(self)
        self.entry3 = Entry(self)

        self.label1.grid(row=1, column=1)
        self.label2.grid(row=2, column=1)
        self.label3.grid(row=3, column=1)

        self.entry1.grid(row=1, column=2)
        self.entry2.grid(row=2, column=2)
        self.entry3.grid(row=3, column=2)

        # Add Button for making selection
        button1 = Button(self, text="OK", command=self.save)
        button1.grid(row=4, column=1)
        button2 = Button(self, text="Anuluj", command=self.cancel)
        button2.grid(row=4, column=2)

    def save(self):
        self.board.mine_count = int(self.entry1.get())
        self.board.width = int(self.entry2.get())
        self.board.height = int(self.entry3.get())
        self.board.retry()
        self.destroy()

    def cancel(self):
        self.destroy()


class SkinChanger(Toplevel):
    def __init__(self, parent, board, **kwargs):
        super().__init__(parent, **kwargs)
        self.board = board
        self.title("Wybór skórki")
        self.skins = os.listdir("Skins")
        self.choice = StringVar(self)
        self.choice.set('default.png')
        self.columnconfigure(1, weight=1)
        self.w = OptionMenu(self, self.choice, *self.skins, command=self.pick)
        self.w.grid(row=1, column=1)

    def pick(self, skin):
        self.board.skin = Skin(os.path.join("Skins", skin), self.board.cell_size)
        self.board.draw_board()
        self.destroy()


def main():
    root = Tk()
    root.columnconfigure(1, weight=1)
    root.rowconfigure(1, weight=1)

    board = Board(root)
    board.grid(row=1, column=1, columnspan=1, sticky='nwes')

    menubar = Menu(root)
    menu = Menu(menubar, tearoff=False)
    menu.add_command(label="Nowa gra", command=lambda: board.retry())
    menu.add_command(label="Trudność", command= lambda: DifficultyPicker(root, board))
    menu.add_command(label="Skórka",  command= lambda: SkinChanger(root, board))
    menu.add_command(label="Ranking")
    menu.add_separator()
    menu.add_command(label="Wyjście", command=root.quit)
    menubar.add_cascade(label="Gra", menu=menu)

    root.config(menu=menubar)

    board.draw_board()
    root.mainloop()


if __name__ == "__main__":
    main()
