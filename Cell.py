class Cell:
    def __init__(self, has_mine, is_uncovered, is_flagged):
        self.mine = has_mine
        self.uncovered = is_uncovered
        self.flagged = is_flagged
        self.mine_count_cache = -1

    def toggle_flagged(self):
        if not self.uncovered:
            self.flagged = not self.flagged

    def uncover(self):
        if not self.flagged:
            self.uncovered = True

