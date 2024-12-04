import pygame
import pygame_shaders

from engine.widget import Widget, PositionedWidget

PERSPECTIVE_VERTEX_SHADER_PATH = "shaders/perspective.vert"
PERSPECTIVE_FRAGMENT_SHADER_PATH = "shaders/perspective.frag"


class PerspectiveWidget(Widget):
    surface: pygame.Surface
    child: PositionedWidget
    shader: pygame_shaders.Shader

    x_rot: float = 0.0
    y_rot: float = 0.0

    def __init__(self, child: PositionedWidget, size: tuple[int, int], enable_mipmaps: bool = False):
        self.child = child
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

        self.shader = pygame_shaders.Shader(
            PERSPECTIVE_VERTEX_SHADER_PATH,
            PERSPECTIVE_FRAGMENT_SHADER_PATH,
            target_surface=self.surface,
            enable_mipmaps=enable_mipmaps)


    def get_size(self) -> tuple[int, int]:
        return self.surface.get_size()


    def __repaint_child(self) -> None:
        self.surface.fill((0, 0, 0, 0))
        self.child.draw_positioned(self.surface)
        print(f"Perspective ({self}): repainted")


    def draw_onto(self,
                  dest: pygame.Surface,
                  top_left: tuple[int, int] | None = None,
                  center: tuple[int, int] | None = None,
                  max_size: tuple[int, int] | None = None,
                  ) -> None:
        if top_left is not None:
            target = top_left
        elif center is not None:
            target = self.surface.get_rect(center=center)
        else:
            assert top_left is not None or center is not None
            return

        should_repaint_child = self.child.parent_should_repaint()
        if should_repaint_child:
            self.__repaint_child()

        self.shader.send("texturePixelSize", self.surface.get_size()[0])
        self.shader.send("x_rot", self.x_rot)
        self.shader.send("y_rot", self.y_rot)
        render = self.shader.render(update_surface=should_repaint_child)

        dest.blit(render, target)
