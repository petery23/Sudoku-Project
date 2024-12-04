import pygame


class Widget:
    def get_size(self) -> tuple[int, int]:
        pass

    def draw_onto(self,
                  screen: pygame.Surface,
                  top_left: tuple[int, int] | None = None,
                  center: tuple[int, int] | None = None,
                  max_size: tuple[int, int] | None = None,
                  ) -> None:
        pass

    def parent_should_repaint(self) -> bool:
        return False


class PositionedWidget(Widget):
    position: tuple[int, int]

    def __init__(self, position: tuple[int, int]):
        self.position = position

    def draw_positioned(self, surface: pygame.Surface) -> None:
        pass