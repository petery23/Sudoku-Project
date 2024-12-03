import pygame

from engine.contexts import UpdateContext, RenderContext
from engine.input import InputState
from engine.scene import Scene


class Engine:
    target_fps: float

    update_context: UpdateContext
    render_context: RenderContext

    active_scene: Scene | None

    def __init__(self, window_name: str, window_size: tuple[int, int], target_fps: float = 60.0):
        self.target_fps = target_fps

        pygame.init()
        pygame.display.set_caption(window_name)
        surface = pygame.display.set_mode(window_size)

        self.update_context = UpdateContext(0.0)
        self.render_context = RenderContext(surface)

        self.active_scene = None

    def main_loop(self):
        clock = pygame.time.Clock()
        input_state = InputState()

        while True:
            ### Process Events
            input_state.start_frame()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                input_state.process_event(event)
            self.update_context.input = input_state
            ###

            ### Update
            self.update_context.dt = 1.0 / self.target_fps
            self.active_scene.update(self.update_context)
            ###

            ### Render
            self.active_scene.render(self.render_context)
            pygame.display.flip()
            ###

            clock.tick(self.target_fps)


    def load_scene(self, scene: Scene | None):
        if self.active_scene is not None:
            self.active_scene.exit_scope()

        self.active_scene = scene
        if self.active_scene is not None:
            self.active_scene.enter_scope()

    def dispose(self):
        self.load_scene(None)
        pygame.quit()