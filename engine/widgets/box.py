import pygame

from engine.widget import Widget


class Box(Widget):
    size: tuple[int, int]
    color: pygame.Color

    def __init__(self, size: tuple[int, int] = (100, 100), color: pygame.Color = pygame.Color(0, 0, 0)):
        self.size = size
        self.color = color

    def get_size(self) -> tuple[int, int]:
        return self.size

    def draw_onto(self,
                  dest: pygame.Surface,
                  top_left: tuple[int, int] | None = None,
                  center: tuple[int, int] | None = None,
                  max_size: tuple[int, int] | None = None,
                  ) -> None:
        size = self.size if max_size is None else (min(max_size[0], self.size[0]), min(max_size[1], self.size[1]))

        if top_left is not None:
            rect = pygame.Rect(top_left[0], top_left[1], size[0], size[1])
        elif center is not None:
            half_size = (size[0] / 2.0, size[1] / 2.0)
            rect = pygame.Rect(center[0] - half_size[0], center[1] - half_size[1], size[0], size[1])
        else:
            assert top_left is not None or center is not None
            return

        pygame.draw.rect(dest, self.color, rect)