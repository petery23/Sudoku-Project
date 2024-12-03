import math

import pygame

from engine.widget import Widget
from engine.widgets.text import Text
from game.sudoku_board import SudokuBoard, SudokuBoardCell


NUMBER_COLOR = pygame.Color(0, 0, 0)
SKETCH_COLOR = pygame.Color(200, 200, 200)


class SudokuBoardWidget(Widget):
    surface: pygame.Surface
    board: SudokuBoard

    cell_number_widgets: list[Text]
    cell_sketch_widgets: list[Text]

    cell_size: tuple[int, int]

    def __init__(self, board: SudokuBoard, ui_size: tuple[int, int]):
        grid_size = board.get_size()
        assert math.isclose(grid_size[0] / grid_size[1], ui_size[0] / ui_size[1]), "grid_size and ui_size must have same aspect ratio!"

        self.cell_number_widgets = []
        self.cell_sketch_widgets = []
        number_font = pygame.font.SysFont("monospace", 16)
        sketch_font = pygame.font.SysFont("monospace", 14)
        for n in range(1, 10):
            self.cell_number_widgets.append(Text(str(n), NUMBER_COLOR, number_font))
            self.cell_sketch_widgets.append(Text(str(n), SKETCH_COLOR, sketch_font))

        self.cell_size = (ui_size[0] // grid_size[0], ui_size[1] // grid_size[1])

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


    def __paint_cell(self, grid_pos: tuple[int, int]) -> None:
        cell = self.board.get_cell(grid_pos)
        display_value, has_number, is_sketch = cell.get_value()
        if not has_number: return

        widget: Text
        if is_sketch: widget = self.cell_sketch_widgets[display_value - 1]
        else: widget = self.cell_number_widgets[display_value - 1]

        screen_pos = (grid_pos[0] * self.cell_size[0] + (self.cell_size[0] // 2), grid_pos[1] * self.cell_size[1] + (self.cell_size[1] // 2))

        widget.draw_onto(self.surface, center=screen_pos)

    def repaint_board(self) -> None:
        self.surface.fill((255, 255, 255))
        width = self.surface.get_width()
        length = self.surface.get_height()
        for i in range(0, width, 75):
            if (i % (75 * 3)) == 0:
                pygame.draw.line(self.surface, "black", (0, i), (length, i), 3)
            pygame.draw.line(self.surface, "black", (0, i), (length, i))
        for i in range(0, length, 75):
            if i % (75 * 3) == 0:
                pygame.draw.line(self.surface, "black", (i, 0), (i, width), 3)
            pygame.draw.line(self.surface, "black", (i, 0), (i, width))

        for x in range(self.board.get_size()[0]):
            for y in range(self.board.get_size()[1]):
                self.__paint_cell((x, y))
