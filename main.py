#!/usr/bin/env python3.9

from DifficultyPicker import DifficultyPicker
from SkinChanger import SkinChanger
from Board import Board
from tkinter import *


def main():
    root = Tk()
    root.columnconfigure(1, weight=1)
    root.rowconfigure(1, weight=1)

    board = Board(root)
    board.grid(row=1, column=1, columnspan=1, sticky='nwes')

    menubar = Menu(root)
    menu = Menu(menubar, tearoff=False)
    menu.add_command(label="Nowa gra", command=lambda: board.retry())
    menu.add_command(label="Trudność", command=lambda: DifficultyPicker(root, board))
    menu.add_command(label="Skórka",  command=lambda: SkinChanger(root, board))
    menu.add_command(label="Ranking")
    menu.add_separator()
    menu.add_command(label="Wyjście", command=root.quit)
    menubar.add_cascade(label="Gra", menu=menu)

    root.config(menu=menubar)

    board.draw_board()
    root.mainloop()


if __name__ == "__main__":
    main()
