from tkinter import *


class DifficultyPicker(Toplevel):
    def __init__(self, parent, board, **kwargs):
        super().__init__(parent, **kwargs)
        self.board = board
        self.title("Wybór trudności")

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
