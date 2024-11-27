from typing import Callable


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
    __state: list[list[int]]

    def __init__(self, state: list[list[int]]):
        super().__init__()

        assert(len(state) >= 3 and len(state) % 3 == 0
               and len(state[0]) >= 3 and len(state[0]) % 3 == 0), "Board size must be divisible by 3"

        self.__state = state

    def get_size(self) -> tuple[int, int]:
        return len(self.__state), len(self.__state[0])

    def change(self):
        self._notify_board_changed(self)
