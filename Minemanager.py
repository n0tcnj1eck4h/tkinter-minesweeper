from Cell import *
from Util import get_surrounding, is_out_of_range
import random


class MineManager:
    def __init__(self, width, height):
        # (Mine, Uncover, Flag)
        self.cells = [[Cell(False, False, False) for x in range(width)] for y in range(height)]
        self.mine_count = 0
        self.cells_uncovered = 0
        self.width = width
        self.height = height
        self.failed = False
        self.populated = False

    def populate(self, mine_count, exclude=(-1, -1), force_no_guessing=False):
        self.mine_count = mine_count
        self.cells = [[Cell(False, False, self.has_flag_at(x, y)) for x in range(self.width)] for y in range(self.height)]
        for i in range(mine_count):
            x, y = 0, 0
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if x == exclude[0] and y == exclude[1]:
                    continue
                if not self.cells[y][x].mine:
                    break
            self.cells[y][x].mine = True
        self.populated = True

    def is_win(self):
        return self.height * self.width - self.mine_count == self.cells_uncovered

    def is_out_of_range(self, x, y):
        return is_out_of_range(x, y, self.width, self.height)

    def has_mine_at(self, x, y):
        return self.cells[y][x].mine

    def has_flag_at(self, x, y):
        return self.cells[y][x].flagged

    def is_uncovered_at(self, x, y):
        return self.cells[y][x].uncovered

    def toggle_flag(self, x, y):
        self.cells[y][x].toggle_flagged()

    def uncover(self, x, y):
        if self.has_mine_at(x, y) and not self.has_flag_at(x, y):
            self.failed = True
        if not self.has_flag_at(x, y) and not self.is_uncovered_at(x, y):
            self.cells[y][x].uncover()
            self.cells_uncovered = self.cells_uncovered + 1
            if self.get_mine_count_around(x, y) == 0:
                for ix, iy in get_surrounding(x, y, self.width, self.height, False):
                    self.uncover(ix, iy)

    def get_mine_count_around(self, x, y):
        if self.is_out_of_range(x, y):
            return 0
        if self.cells[y][x].mine_count_cache != -1:
            return self.cells[y][x].mine_count_cache
        count = 0
        for ix, iy in get_surrounding(x, y, self.width, self.height, True):
            if self.has_mine_at(ix, iy):
                count = count + 1
        self.cells[y][x].mine_count_cache = count
        return count

    def get_flag_count_around(self, x, y):
        count = 0
        for ix, iy in get_surrounding(x, y, self.width, self.height, False):
            if self.has_flag_at(ix, iy):
                count = count + 1
        return count

    def uncover_remaining(self, x, y):
        if self.get_flag_count_around(x, y) == self.get_mine_count_around(x, y):
            for ix, iy in get_surrounding(x, y, self.width, self.height, False):
                if self.has_flag_at(ix, iy):
                    continue
                self.uncover(ix, iy)
