import PIL.Image
from PIL import Image, ImageTk


class Skin:
    def __init__(self, filename, size):
        self.image = Image.open(filename)
        self.cell_size = self.image.height // 2
        self.size = size
        self.number = []
        self.mine_incorrect = None
        self.cell_covered = None
        self.mine_clicked = None
        self.flag = None
        self.mine = None
        self.reload(size)

    def reload(self, size):
        self.cell_size = self.image.height // 2
        self.number = []
        self.size = size
        for i in range(9):
            self.number.insert(i, self.get(i, 0))
        self.cell_covered = self.get(0, 1)
        self.flag = self.get(1, 1)
        self.mine_clicked = self.get(2, 1)
        self.mine_incorrect = self.get(3, 1)
        self.mine = self.get(4, 1)

    def get(self, x, y):
        image = self.image.crop((x * self.cell_size,                        y * self.cell_size,
                                 x * self.cell_size + self.cell_size - 1,   y * self.cell_size + self.cell_size - 1))
        image = image.resize((self.size, self.size))
        return ImageTk.PhotoImage(image)



