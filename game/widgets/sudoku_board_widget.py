import math

import pygame

from engine.widget import Widget
from game.sudoku_board import SudokuBoard


class SudokuBoardWidget(Widget):
    surface: pygame.Surface
    board: SudokuBoard

    def __init__(self, board: SudokuBoard, ui_size: tuple[int, int]):
        grid_size = board.get_size()
        assert math.isclose(grid_size[0] / grid_size[1], ui_size[0] / ui_size[1]), "grid_size and ui_size must have same aspect ratio!"

        self.surface = pygame.Surface(ui_size)
        self.board = board
        self.repaint_board()


    def get_size(self) -> tuple[int, int]:
        return self.surface.get_size()

    def draw_onto(self,
                  screen: pygame.Surface,
                  top_left: tuple[int, int] | None = None,
                  center: tuple[int, int] | None = None,
                  max_size: tuple[int, int] | None = None,
                  ) -> None:
        if top_left is not None:
            target = top_left
        elif center is not None:
            target = self.surface.get_rect(center=center)
        else:
            assert top_left is not None or center is not None
            return

        screen.blit(self.surface, target)


    def repaint_board(self) -> None:
        self.surface.fill((255, 255, 255))
        width = self.surface.get_width()
        length = self.surface.get_height()
        for i in range(0, width, 75):
            if (i % (75 * 3)) == 0:
                pygame.draw.line(self.surface, "black", (0, i), (length, i), 3)
            pygame.draw.line(self.surface, "black", (0, i), (length, i))
        for i in range(0, length, 75):
            if (i % (75 * 3) == 0):
                pygame.draw.line(self.surface, "black", (i, 0), (i, width), 3)
            pygame.draw.line(self.surface, "black", (i, 0), (i, width))

