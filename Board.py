from Util import get_surrounding, is_out_of_range
from tkinter import messagebox
from Minemanager import *
from tkinter import *
from Skin import *
import math


class Board(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.width = 30
        self.height = 20
        self.mine_count = 60
        self.cell_size = 40
        self.m1held = False
        self.m2held = False
        self.handle_input = True
        self.sprite_cache = [[None for x in range(self.width)] for y in range(self.height)]

        self.mine_manager = MineManager(self.width, self.height)

        self.skin = Skin("Skins/default.png", self.cell_size)

        self.bind("<Button-1>", self._m1down)
        self.bind("<ButtonRelease-1>", self._m1release)
        self.bind("<B1-Motion>", self._m1motion)
        self.bind("<Button-3>", self._m2down)
        self.bind("<ButtonRelease-3>", self._m2release)
        self.bind("<Configure>", self._resize)

    def retry(self):
        self.clear_sprite_cache()
        self.mine_manager = MineManager(self.width, self.height)
        self.draw_board()
        self.handle_input = True

    def get_clicked_square(self, event):
        x = math.floor(event.x / self.cell_size)
        y = math.floor(event.y / self.cell_size)
        return x, y

    def clear_sprite(self, x, y):
        if self.sprite_cache[y][x] is not None:
            self.delete(self.sprite_cache[y][x])
            self.sprite_cache[y][x] = None

    def clear_sprite_cache(self):
        for y in self.sprite_cache:
            for x in y:
                self.delete(x)
        self.sprite_cache = [[None for x in range(self.width)] for y in range(self.height)]

    def draw_square(self, x, y, fill):
        self.clear_sprite(x, y)
        self.sprite_cache[y][x] = self.create_rectangle(x * self.cell_size, y * self.cell_size, (x + 1) * self.cell_size,
                                                        (y + 1) * self.cell_size, fill=fill)

    def draw_image(self, x, y, image):
        self.clear_sprite(x, y)
        self.sprite_cache[y][x] = self.create_image(x * self.cell_size, y * self.cell_size, image=image, anchor='nw')

    def draw_board(self):
        for y in range(self.height):
            for x in range(self.width):
                mine = self.mine_manager.cells[y][x]
                if not mine.uncovered:
                    if mine.flagged:
                        self.draw_image(x, y, self.skin.flag)
                    else:
                        self.draw_image(x, y, self.skin.cell_covered)
                else:
                    if mine.mine:
                        self.draw_image(x, y, self.skin.mine)
                    else:
                        self.draw_image(x, y, self.skin.number[self.mine_manager.get_mine_count_around(x, y)])

    def draw_hover(self, event):
        x, y = self.get_clicked_square(event)
        if is_out_of_range(x, y, self.width, self.height):
            return
        if self.m1held:
            if self.mine_manager.is_uncovered_at(x, y):
                for x, y in get_surrounding(x, y, self.width, self.height, True):
                    if not self.mine_manager.is_uncovered_at(x, y) and not self.mine_manager.has_flag_at(x, y):
                        self.draw_image(x, y, self.skin.number[0])
            else:
                if not self.mine_manager.is_uncovered_at(x, y) and not self.mine_manager.has_flag_at(x, y):
                    self.draw_image(x, y, self.skin.number[0])

    def draw_fail(self):
        for y in range(self.height):
            for x in range(self.width):
                mine = self.mine_manager.cells[y][x]
                if mine.mine and not mine.flagged:
                    self.draw_image(x, y, self.skin.mine)
                if mine.mine and mine.uncovered:
                    self.draw_image(x, y, self.skin.mine_clicked)
                if mine.flagged and not mine.mine:
                    self.draw_image(x, y, self.skin.mine_incorrect)

    def draw_win(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.mine_manager.cells[y][x].mine:
                    self.draw_image(x, y, self.skin.flag)

    def _m1down(self, event):
        if not self.handle_input:
            return
        self.m1held = True
        self.draw_board()
        self.draw_hover(event)

    def _m1release(self, event):
        if not self.handle_input:
            return

        x, y = self.get_clicked_square(event)
        if is_out_of_range(x, y, self.width, self.height):
            return

        if not self.mine_manager.populated:
            self.mine_manager.populate(self.mine_count, (x, y))

        self.m1held = False
        if self.mine_manager.is_uncovered_at(x, y):
            self.mine_manager.uncover_remaining(x, y)
        else:
            self.mine_manager.uncover(x, y)

        self.draw_board()

        if self.mine_manager.failed:
            self.handle_input = False
            self.draw_fail()
        elif self.mine_manager.is_win():
            self.handle_input = False
            self.draw_win()
            messagebox.showinfo("Wygrana!", "Twój czas to: {}s"
                                .format(round(time.time() - self.mine_manager.populated_timestamp)))

    def _m1motion(self, event):
        if not self.handle_input:
            return
        self.draw_board()
        self.draw_hover(event)

    def _m2down(self, event):
        if not self.handle_input:
            return

        x, y = self.get_clicked_square(event)
        if not is_out_of_range(x, y, self.width, self.height):
            self.mine_manager.toggle_flag(x, y)

        self.m2held = True
        self.draw_board()

    def _m2release(self, event):
        if not self.handle_input:
            return
        self.m2held = False
        self.draw_board()

    def _resize(self, event):
        self.cell_size = min(event.width // self.width, event.height // self.height)
        self.skin.reload(self.cell_size)
        self.draw_board()
        if self.mine_manager.failed:
            self.draw_fail()
        elif self.mine_manager.is_win():
            self.draw_win()

