from Skin import Skin
from tkinter import *
import os


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
