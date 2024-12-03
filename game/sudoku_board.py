
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

    def set_value(self, value: int = 0, clear: bool = False, is_sketch: bool = False):
        if self.__given: return
        if clear or value == 0:
            self.__value = 0
            return
        if value < 1 or value > 9: raise ValueError("Number not in range")

        self.__value = value * (-1 if is_sketch else 1)

    def get_value(self) -> tuple[int, bool, bool]:

        """
        Returns:
            - int The number to display
            - bool True if cell is not empty
            - bool True if cell contains a sketch
        """
        match self.__value:
            case 0:
                return 0, False, False
            case x if x > 0:
                return x, True, False
            case x if x < 0:
                return -x, True, True

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
                self.__state[x].append(SudokuBoardCell(state[x][y],given=True))

    def get_size(self) -> tuple[int, int]:
        return len(self.__state), len(self.__state[0])

    def get_cell(self, grid_pos: tuple[int, int]) -> SudokuBoardCell:
        return self.__state[grid_pos[0]][grid_pos[1]]

    def set_cell(self, grid_pos: tuple[int, int], cell: SudokuBoardCell):
        self.__state[grid_pos[0]][grid_pos[1]] = cell
        self.force_notify_change()

    def __valid_cell(self, row: int, col: int, cell: SudokuBoardCell):
        """
        Determines if num is contained in the specified row (horizontal) of the board
        If num is already in the specified row, return False. Otherwise, return True

        Parameters:
        row is the index of the row we are checking
        num is the value we are looking for in the row

        Return: boolean
        """
        size = self.get_size()[0]

        # checks row
        for col in range(size):
            if self.__state[row][col] == cell:
                return False


        # checks col
        for row in range(size):
            if self.__state[row][col] == cell:
                return False

        # checks box
        row_start = (row//3)*3
        col_start = (col//3)*3
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.__state[row][col] == cell:
                    return False

        # number is valid
        return True

    def player_validate_set_cell(self, grid_pos: tuple[int, int], cell: SudokuBoardCell) -> bool:
        if self.__difficulty==SudokuDifficulty.EASY:
            if cell.get_value()[0] == self.__state[grid_pos[0]][grid_pos[1]]:
                return True
            else:
                return False
        if self.__difficulty==SudokuDifficulty.MEDIUM or self.__difficulty==SudokuDifficulty.HARD:
            return self.__valid_cell(grid_pos[0], grid_pos[1], cell)


    def force_notify_change(self):
        self._notify_board_changed(self)
