def is_out_of_range(x, y, board_width, board_height):
    return x not in range(0, board_width) or y not in range(0, board_height)


def get_surrounding(x, y, board_width, board_height, include_middle=False):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if is_out_of_range(x + i, y + j, board_width, board_height):
                continue
            if not include_middle and i == j == 0:
                continue
            yield x + i, y + j

