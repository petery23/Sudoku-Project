import pygame

from engine.widget import PositionedWidget, Widget


class Positioned(PositionedWidget):
    child: Widget

    def __init__(self, position: tuple[int, int], child: Widget):
        super().__init__(position)
        self.child = child

    def get_size(self) -> tuple[int, int]:
        return self.child.get_size()

    def draw_positioned(self, surface: pygame.Surface) -> None:
        self.child.draw_onto(surface, center=self.position)