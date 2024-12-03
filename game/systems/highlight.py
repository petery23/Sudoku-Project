from engine.contexts import UpdateContext, RenderContext
from game.widgets.sudoku_board_widget import SudokuBoardWidget


class System:

    def __init__(self, board_widget: SudokuBoardWidget):
        self.selected_cell = (-1,-1)
        self.board_widget = board_widget
        self.cell_size = board_widget.get_size()[0]/board_widget.board.get_size()[0]
    def enter_scope(self):
        pass

    def update(self, context: UpdateContext):
        # finds cell being hovered over
        x,y = context.input.mouse_pos
        self.selected_cell = (int(x/self.cell_size),int(y/self.cell_size))

    def render(self, context: RenderContext):
        # board is centered
        # context.surface.get_size() gives pixel size of entire screen
        # context.surface.get_size()
        # draws outline around hovered cell

        top_left_x = (context.surface.get_size()[0]-self.board_widget.get_size()[0])/2
        top_left_y = (context.surface.get_size()[1]-self.board_widget.get_size()[0])/2

        hovered_x = top_left_x + self.selected_cell[0]*self.cell_size
        hovered_y = top_left_y + self.selected_cell[1]*self.cell_size

        pygame
        pass

    def exit_scope(self):
        pass

    def dispose(self):
        pass