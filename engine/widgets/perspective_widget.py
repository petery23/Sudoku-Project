import pygame
import pygame_shaders

from engine.widget import Widget

PERSPECTIVE_VERTEX_SHADER_PATH = "shaders/perspective.vert"
PERSPECTIVE_FRAGMENT_SHADER_PATH = "shaders/perspective.frag"


class PerspectiveWidget(Widget):
    surface: pygame.Surface
    child: Widget
    shader: pygame_shaders.Shader

    x_rot: float = 0.0
    y_rot: float = 0.0

    def __init__(self, child: Widget):
        self.child = child

        inner_size = child.get_size()
        self.surface = pygame.Surface((inner_size[0], inner_size[1]), pygame.SRCALPHA)

        self.shader = pygame_shaders.Shader(
            PERSPECTIVE_VERTEX_SHADER_PATH,
            PERSPECTIVE_FRAGMENT_SHADER_PATH,
            target_surface=self.surface)


    def get_size(self) -> tuple[int, int]:
        return self.surface.get_size()


    def __repaint_child(self) -> None:
        self.surface.fill((0, 0, 0, 0))
        self.child.draw_onto(self.surface, top_left=(0, 0))
        print("Repainted")


    def draw_onto(self,
                  screen: pygame.Surface,
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

        #self.shader.send("texturePixelSize", self.surface.get_size()[0])
        self.shader.send("x_rot", self.x_rot)
        self.shader.send("y_rot", self.y_rot)
        render = self.shader.render(update_surface=should_repaint_child)

        screen.blit(render, target)
