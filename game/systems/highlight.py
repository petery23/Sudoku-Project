import pygame

from engine.contexts import UpdateContext, RenderContext
from engine.system import System
from game.widgets.sudoku_board_widget import SudokuBoardWidget

HIGHLIGHT_PURPLE = (128,0,128)
HIGHLIGHT_WIDTH = 4

class HighlightSystem(System):

    def __init__(self, board_widget: SudokuBoardWidget):
        self.selected_cell = (-1,-1)
        self.board_widget = board_widget
        self.cell_size = board_widget.get_size()[0]/(board_widget.board.get_size()[0]+1)
        self.mouse_x = -1
        self.mouse_y = -1
    def enter_scope(self):
        pass

    def update(self, context: UpdateContext):
        # finds cell being hovered over
        self.mouse_x,self.mouse_y = context.input.mouse_pos

    def render(self, context: RenderContext):
        # board is centered
        # context.surface.get_size() gives pixel size of entire screen
        # context.surface.get_size()
        # draws outline around hovered cell

        top_left_x = (context.surface.get_size()[0]-self.board_widget.get_size()[0])/2
        top_left_y = (context.surface.get_size()[1]-self.board_widget.get_size()[0])/2

        self.selected_cell = (int((self.mouse_x-top_left_x) / self.cell_size), int((self.mouse_y-top_left_y) / self.cell_size))




        hovered_x = top_left_x + self.selected_cell[0]*self.cell_size
        hovered_y = top_left_y + self.selected_cell[1]*self.cell_size

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