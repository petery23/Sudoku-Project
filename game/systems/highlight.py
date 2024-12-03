import pygame

from engine.contexts import UpdateContext, RenderContext
from engine.system import System
from game.widgets.sudoku_board_widget import SudokuBoardWidget

HIGHLIGHT_PURPLE = (128,0,128)
HIGHLIGHT_WIDTH = 4

class HighlightSystem(System):

    def __init__(self, board_widget: SudokuBoardWidget):
        self.top_left_y = 0
        self.top_left_x = 0
        self.selected_cell = (-1,-1)
        self.board_widget = board_widget
        self.cell_size = board_widget.get_size()[0]/(board_widget.board.get_size()[0])

    def enter_scope(self):
        pass

    def update(self, context: UpdateContext):
        if abs(context.input.mouse_delta[0]) + abs(context.input.mouse_delta[1]) >= 1:
            # mouse has moved
            # finds cell being hovered over
            self.top_left_x = (context.screenSize[0] - self.board_widget.get_size()[0]) / 2
            self.top_left_y = (context.screenSize[1] - self.board_widget.get_size()[0]) / 2

            mouse_x, mouse_y = context.input.mouse_pos

            self.selected_cell = (int((mouse_x - self.top_left_x) / self.cell_size), int((mouse_y - self.top_left_y) / self.cell_size))
        else:
            # mouse hasn't moved, defer to arrow keys
            pass




    def render(self, context: RenderContext):
        # board is centered
        # context.surface.get_size() gives pixel size of entire screen
        # context.surface.get_size()
        # draws outline around hovered cell

        hovered_x = self.top_left_x + self.selected_cell[0]*self.cell_size
        hovered_y = self.top_left_y + self.selected_cell[1]*self.cell_size

        pygame.draw.lines(context.surface,
                          HIGHLIGHT_PURPLE,
                          True,
                          [(hovered_x,hovered_y), (hovered_x+self.cell_size,hovered_y),
                          (hovered_x+self.cell_size,hovered_y+self.cell_size), (hovered_x,hovered_y+self.cell_size)],
                          HIGHLIGHT_WIDTH)

        pass

    def exit_scope(self):
        pass

    def dispose(self):
        pass