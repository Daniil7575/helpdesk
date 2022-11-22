# import random


# class Cell:
#     def __init__(self, around_mines: int = 0, mine: bool = False) -> None:
#         self.around_mines = around_mines
#         self.mine = mine
#         self.fl_open = False


# class GamePole:
#     def __init__(self, n, m) -> None:
#         self.m = m
#         self.side = n
#         self.pole = [[Cell() for _ in range(n)] for _ in range(n)]
#         self.mines = set()
#         self.init()
#         self._set_around_mines_attrs()

#     def init(self):
#         mines = random.sample(range(self.side ** 2), self.m)
#         for mine in mines:
#             row = mine // self.side
#             cell = mine % self.side
#             self.mines.add((cell, row))
#             self.pole[row][cell].mine = True

#     def show(self):
#         for i in range(self.side):
#             for j in range(self.side):
#                 cell = self.pole[i][j]
#                 print(cell.around_mines if not cell.mine else '#', end='')
#             print()

#     def _set_around_mines_attrs(self):
#         coords_delta = (
#             (-1, -1), (0, -1), (1, -1),
#             (-1, 0), (1, 0),
#             (-1, 1), (0, 1), (1, 1),
#         )
#         for x, y in self.mines:
#             for dx, dy in coords_delta:
#                 if -1 < (x + dx) < self.side and -1 < (y + dy) < self.side:
#                     self.pole[y + dy][x + dx].around_mines += 1


# game = GamePole(10, 12)
# game.show()



