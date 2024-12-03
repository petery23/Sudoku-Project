import enum

import pygame.event


class MouseState(enum.Enum):
    NONE = 0,
    DOWN = 1,
    DRAGGING = 2,
    UP = 3,


class InputState:
    mouse_pos: tuple[int, int]
    mouse_delta: tuple[int, int]

    mouse_state: MouseState
    mouse_down_pos: tuple[int, int]
    mouse_up_pos: tuple[int, int]

    def __init__(self):
        self.mouse_pos = (0, 0)

        self.mouse_state = MouseState.NONE
        self.mouse_down_pos = (0, 0)
        self.mouse_up_pos = (0, 0)

    def start_frame(self):
        # Calculate mouse position delta since last frame
        new_mouse_pos = pygame.mouse.get_pos()
        self.mouse_delta = (new_mouse_pos[0] - self.mouse_pos[0], new_mouse_pos[1] - self.mouse_pos[1])
        self.mouse_pos = new_mouse_pos

    def process_event(self, event: pygame.event.Event):
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