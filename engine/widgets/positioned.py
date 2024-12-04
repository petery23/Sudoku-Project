import pygame

from engine.widget import PositionedWidget, Widget


class Positioned(PositionedWidget):
    child: Widget

    __dirty: bool

    def __init__(self, position: tuple[int, int], child: Widget):
        super().__init__(position)
        self.child = child

        self.__dirty = False

    def get_size(self) -> tuple[int, int]:
        return self.child.get_size()

    def draw_positioned(self, surface: pygame.Surface) -> None:
        self.child.draw_onto(surface, center=self.position)

    def make_dirty(self) -> None:
        self.__dirty = True

    def parent_should_repaint(self) -> bool:
        if self.__dirty:
            self.__dirty = False
            return True
        return False