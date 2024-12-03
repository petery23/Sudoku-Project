from typing import Callable


class SudokuBoardCell:
    __value: int

    def __init__(self, value: int = 0, is_sketch: bool = False):
        # empty tiles are 0
        # sketch values are negative
        self.__value = value * (-1 if is_sketch else 1)

    def get_value(self) -> tuple[int, bool, bool]:
        """
        Returns:
            1: number to display
            2: true if cell is not empty
            3: true if cell contains a sketch
        """
        match self.__value:
            case 0:
                return 0, False, False
            case x if x > 0:
                return x, True, False
            case x if x < 0:
                return -x, True, True


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

    def __init__(self, state: list[list[int]], solution: list[list[int]]):
        super().__init__()
        self.__solution = solution

        assert(len(state) >= 3 and len(state) % 3 == 0
               and len(state[0]) >= 3 and len(state[0]) % 3 == 0), "Board size must be divisible by 3"

        self.__state = []
        for x in range(len(state)):
            self.__state.append([])
            for y in range(len(state[x])):
                self.__state[x].append(SudokuBoardCell(state[x][y]))

    def get_size(self) -> tuple[int, int]:
        return len(self.__state), len(self.__state[0])

    def get_cell(self, grid_pos: tuple[int, int]) -> SudokuBoardCell:
        return self.__state[grid_pos[0]][grid_pos[1]]

    def set_cell(self, grid_pos: tuple[int, int], cell: SudokuBoardCell):
        self.__state[grid_pos[0]][grid_pos[1]] = cell
        self.force_notify_change()

    def player_set_cell(self, grid_pos: tuple[int, int], cell):
        pass

    def force_notify_change(self):
        self._notify_board_changed(self)
