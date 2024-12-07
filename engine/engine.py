import pygame
import pygame_shaders

from engine.contexts import UpdateContext, RenderContext, SceneChangeContext
from engine.input import InputState
from engine.scene import Scene

# To check OS
import platform

class Engine:
    target_fps: float

    display: pygame.Surface
    surface: pygame.Surface
    screen_shader: pygame_shaders.Shader

    input_state: InputState

    active_scene: Scene | None

    def __init__(self, window_name: str, window_size: tuple[int, int], target_fps: float = 60.0):
        self.target_fps = target_fps

        pygame.init()
        pygame.display.set_caption(window_name)

        #pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        #pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)

        # Check if OS is mac to request core profile or else openGL won't work
        if platform.system() == 'Darwin':
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)

        # pygame.OPENGL flag allows the use of custom shaders

        self.display = pygame.display.set_mode(window_size, pygame.OPENGL | pygame.DOUBLEBUF)
        self.surface = pygame.Surface(self.display.get_size())
        self.screen_shader = pygame_shaders.DefaultScreenShader(self.surface)

        self.input_state = InputState()

        self.active_scene = None

    def main_loop(self):
        clock = pygame.time.Clock()
        time = 0.0

        update_context = UpdateContext(0.0,0.0, self.display.get_size(), self.input_state)
        render_context = RenderContext(0.0, self.surface)

        while True:
            time += clock.get_time() / 1000
            dt = 1.0 / self.target_fps

            ### Process Events
            self.input_state.start_frame()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                self.input_state.process_event(event)
            ###

            ### Update
            update_context.time = time
            update_context.dt = dt
            self.active_scene.update(update_context)
            ###

            ### Render
            render_context.time = time
            self.active_scene.render(render_context)

            self.screen_shader.render()
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
