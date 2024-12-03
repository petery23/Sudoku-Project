import pygame

from engine.contexts import UpdateContext, RenderContext, SceneChangeContext
from engine.input import InputState
from engine.scene import Scene


class Engine:
    target_fps: float
    surface: pygame.Surface

    input_state: InputState

    active_scene: Scene | None

    def __init__(self, window_name: str, window_size: tuple[int, int], target_fps: float = 60.0):
        self.target_fps = target_fps

        pygame.init()
        pygame.display.set_caption(window_name)
        self.surface = pygame.display.set_mode(window_size)

        self.input_state = InputState()

        self.active_scene = None

    def main_loop(self):
        clock = pygame.time.Clock()

        update_context = UpdateContext(0.0, self.surface.get_size(), self.input_state)
        render_context = RenderContext(self.surface)

        while True:
            ### Process Events
            self.input_state.start_frame()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                self.input_state.process_event(event)
            ###

            ### Update
            update_context.dt = 1.0 / self.target_fps
            self.active_scene.update(update_context)
            ###

            ### Render
            self.active_scene.render(render_context)
            pygame.display.flip()
            ###

            clock.tick(self.target_fps)


    def load_scene(self, scene: Scene | None):
        self.input_state.clear()
        context = SceneChangeContext(self.input_state)

        if self.active_scene is not None:
            self.active_scene.exit_scope(context)

        self.active_scene = scene
        if self.active_scene is not None:
            self.active_scene.enter_scope(context)

    def dispose(self):
        self.load_scene(None)
        pygame.quit()