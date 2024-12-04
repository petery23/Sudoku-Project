import pygame


class Widget:
    def get_size(self) -> tuple[int, int]:
        pass

    def draw_onto(self,
                  dest: pygame.Surface,
                  top_left: tuple[int, int] | None = None,
                  center: tuple[int, int] | None = None,
                  max_size: tuple[int, int] | None = None,
                  ) -> None:
        pass

    def make_dirty(self):
        """

        Sets the widget's dirty flag to True.
        Use parent_should_repaint to check and clear the flag.

        """
        pass

    def parent_should_repaint(self) -> bool:
        """

        Clears the widget's dirty flag.

        Returns:
            True if the widget is dirty

        """
        return False


class PositionedWidget(Widget):
    position: tuple[int, int]

    def __init__(self, position: tuple[int, int]):
        self.position = position

    def draw_positioned(self, surface: pygame.Surface) -> None:
        pass