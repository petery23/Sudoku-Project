import enum
from typing import Callable

import pygame.event

class KeyboardAction(enum.Enum):
    DOWN = 0,
    UP = 1,

class KeyboardEvent:
    action: KeyboardAction
    key: int

    def __init__(self, action: KeyboardAction, key: int):
        self.action = action
        self.key = key

KeyboardObserver = Callable[[KeyboardEvent], None]

class KeyboardSubject:
    __observers: list[KeyboardObserver]

    def __init__(self):
        self.__observers = []

    def add_observer(self, observer: KeyboardObserver):
        self.__observers.append(observer)

    def remove_observer(self, observer: KeyboardObserver):
        self.__observers.remove(observer)

    def _notify_event(self, event: KeyboardEvent):
        for observer in self.__observers:
            observer(event)



class MouseState(enum.Enum):
    NONE = 0,
    DOWN = 1,
    DRAGGING = 2,
    UP = 3,


class InputState(KeyboardSubject):
    mouse_pos: tuple[int, int]
    mouse_delta: tuple[int, int]

    mouse_state: MouseState
    mouse_down_pos: tuple[int, int]
    mouse_up_pos: tuple[int, int]

    def __init__(self):
        super().__init__()
        self.clear()

    def start_frame(self):
        # Calculate mouse position delta since last frame
        new_mouse_pos = pygame.mouse.get_pos()
        self.mouse_delta = (new_mouse_pos[0] - self.mouse_pos[0], new_mouse_pos[1] - self.mouse_pos[1])
        self.mouse_pos = new_mouse_pos

        match self.mouse_state:
            case MouseState.DOWN:
                self.mouse_state = MouseState.DRAGGING
            case MouseState.UP:
                self.mouse_state = MouseState.NONE

    def process_event(self, event: pygame.event.Event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                self.mouse_down_pos = event.pos
                self.mouse_state = MouseState.DOWN
            case pygame.MOUSEBUTTONUP:
                self.mouse_up_pos = event.pos
                self.mouse_state = MouseState.UP

            case pygame.KEYDOWN:
                self._notify_event(KeyboardEvent(KeyboardAction.DOWN, event.key))
            case pygame.KEYUP:
                self._notify_event(KeyboardEvent(KeyboardAction.UP, event.key))

    def clear(self):
        self.mouse_pos = (0, 0)
        self.mouse_delta = (0, 0)

        self.mouse_state = MouseState.NONE
        self.mouse_down_pos = (0, 0)
        self.mouse_up_pos = (0, 0)