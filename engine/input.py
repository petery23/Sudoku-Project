import enum

import pygame.event


class MouseState(enum.Enum):
    NONE = 0,
    DOWN = 1,
    DRAGGING = 2,
    UP = 3,


class InputState:
    mouse_pos: tuple[int, int]

    mouse_state: MouseState
    mouse_down_pos: tuple[int, int]
    mouse_up_pos: tuple[int, int]

    def __init__(self):
        self.mouse_pos = (0, 0)

        self.mouse_state = MouseState.NONE
        self.mouse_down_pos = (0, 0)
        self.mouse_up_pos = (0, 0)

    def process_event(self, event: pygame.event.Event):
        self.mouse_pos = pygame.mouse.get_pos()

        match self.mouse_state:
            case MouseState.DOWN:
                self.mouse_state = MouseState.DRAGGING
            case MouseState.UP:
                self.mouse_state = MouseState.NONE

        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                self.mouse_down_pos = event.pos
                self.mouse_state = MouseState.DOWN
            case pygame.MOUSEBUTTONUP:
                self.mouse_up_pos = event.pos
                self.mouse_state = MouseState.UP