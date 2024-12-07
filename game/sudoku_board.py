
from typing import Callable

from game.sudoku_difficulty import SudokuDifficulty
from sudoku_generator import SudokuGenerator


class SudokuBoardCell:
    __value: int
    __given: bool

    def __init__(self, value: int = 0, is_sketch: bool = False, given: bool = False):
        # empty tiles are 0
        # sketch values are negative
        if value < 0 or value > 9: raise ValueError("Number not in range")
        self.__value = value * (-1 if is_sketch else 1)
        self.__given = given

    def is_given(self):
        return self.__given

    def set_value(self, value: int = 0, clear: bool = False, is_sketch: bool = False) -> bool:
        """

        Args:
            value:
            clear:
            is_sketch:

        Returns:
            True if the cell was changed

        """
        if self.__given: return False
        if clear or value == 0:
            if self.__value != 0:
                self.__value = 0
                return True
            return False
        if value < 1 or value > 9: raise ValueError("Number not in range")

        new_value = value * (-1 if is_sketch else 1)
        if self.__value != new_value:
            self.__value = new_value
            return True

        return False


    def get_value(self) -> tuple[int, bool, bool]:
        """
        Returns:
            - int The number to display
            - bool True if cell is empty
            - bool True if cell contains a sketch
        """
        match self.__value:
            case 0:
                return 0, True, False
            case x if x > 0:
                return x, False, False
            case x if x < 0:
                return -x, False, True

    def __eq__(self, other):
        if isinstance(other, SudokuBoardCell):
            return other.__value == self.__value
        return False


class SudokuBoard: pass
SudokuBoardObserver = Callable[[SudokuBoard], None]

class SudokuBoardSubject:
    __observers: list[SudokuBoardObserver]

    def __init__(self):
        self.__observers = []

    def add_observer(self, observer: SudokuBoardObserver):
        self.__observers.append(observer)

    def remove_observer(self, observer: SudokuBoardObserver):
        self.__observers.remove(observer)

    def _notify_board_changed(self, new_state: SudokuBoard):
        for observer in self.__observers:
            observer(new_state)


class SudokuBoard(SudokuBoardSubject):
    __state: list[list[SudokuBoardCell]]
    __solution: list[list[int]]
    __difficulty: SudokuDifficulty

    def __init__(self, state: list[list[int]], solution: list[list[int]], difficulty: SudokuDifficulty):
        super().__init__()
        self.__solution = solution
        self.__difficulty = difficulty

        assert(len(state) >= 3 and len(state) % 3 == 0
               and len(state[0]) >= 3 and len(state[0]) % 3 == 0), "Board size must be divisible by 3"

        self.__state = []
        for x in range(len(state)):
            self.__state.append([])
            for y in range(len(state[x])):
                self.__state[x].append(SudokuBoardCell(state[x][y],given=state[x][y]!=0))

    def is_full(self) -> bool:
        for row in self.__state:
            for cell in row:
                if cell.get_value()[1]:
                    return False
        return True

    def is_solved(self) -> bool:
        for i, row in enumerate(self.__state):
            for j, cell in enumerate(row):
                if cell.get_value()[0] != self.__solution[i][j]:
                    return False
        return True

    def get_size(self) -> tuple[int, int]:
        return len(self.__state), len(self.__state[0])

    def get_cell(self, grid_pos: tuple[int, int]) -> SudokuBoardCell:
        return self.__state[grid_pos[0]][grid_pos[1]]

    def set_cell(self, grid_pos: tuple[int, int], value: int = 0, clear: bool = False, is_sketch: bool = False) -> bool:
        """

        Args:
            grid_pos:
            value:
            clear:
            is_sketch:

        Returns:
            True if cell was changed

        """

        cell = self.__state[grid_pos[0]][grid_pos[1]]
        previous = cell.get_value()

        changed = cell.set_value(value, clear, is_sketch)
        if not changed:
            return False
        else:
            self.notify_change()

        # if self.validate_cell(grid_pos, cell):
        #     # new cell state is valid
        #     return True
        # else:
        #     # new cell state is invalid, restore it to its previous state
        #     if not cell.set_value(*previous): raise Exception("Cell had corrupted state when attempting to set its value.")
        #     return False

    def validate_cell(self, grid_pos: tuple[int, int]):
        """
        Determines if num is contained in the specified row (horizontal) of the board
        If num is already in the specified row, return False. Otherwise, return True

        Parameters:
        row is the index of the row we are checking
        num is the value we are looking for in the row

        Return: boolean
        """
        cell = self.get_cell(grid_pos)
        size = self.get_size()[0]

        # checks row
        for col in range(size):
            if self.__state[grid_pos[0]][col] == cell:
                if col!=grid_pos[1]:
                    return False


        # checks col
        for row in range(size):
            if self.__state[row][grid_pos[1]] == cell:
                if row!=grid_pos[0]:
                    return False

        # checks box
        row_start = (grid_pos[0]//3)*3
        col_start = (grid_pos[1]//3)*3
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if row == grid_pos[0] and col == grid_pos[1]:
                    continue
                if self.__state[row][col] == cell:
                    return False

        # number is valid
        return True

    # def validate_cell(self, grid_pos: tuple[int, int], cell: SudokuBoardCell) -> bool:
    #     if self.__difficulty==SudokuDifficulty.EASY:
    #         if cell.get_value()[0] == self.__state[grid_pos[0]][grid_pos[1]]:
    #             return True
    #         else:
    #             return False
    #     if self.__difficulty==SudokuDifficulty.MEDIUM or self.__difficulty==SudokuDifficulty.HARD:
    #         return self.__valid_cell(grid_pos, cell)


    def notify_change(self):
        self._notify_board_changed(self)


    def get_difficulty(self):
        return self.__difficulty
