import pygame.event


class InputState:
    clicks = list[tuple[int, int]]

    def __init__(self):
        self.clicks = []

    def process_event(self, event: pygame.event.Event):
        match event.type:
            case pygame.MOUSEBUTTONUP:
                self.clicks.append(event.pos)