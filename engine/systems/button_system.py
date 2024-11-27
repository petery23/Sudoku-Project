from engine.engine import UpdateContext, RenderContext
from engine.input import MouseState
from engine.system import System
from engine.widgets.button import Button


class ButtonSystem(System):
    buttons: list[Button]
    buttons_pressed: list[Button]

    def __init__(self, buttons: list[Button]):
        self.buttons = buttons
        self.buttons_pressed = []

    def enter_scope(self):
        pass

    def update(self, context: UpdateContext):
        match context.input.mouse_state:
            case MouseState.DOWN:
                self.buttons_pressed = []
                for button in self.buttons:
                    if not button.interactable: continue
                    if not button.rect.collidepoint(context.input.mouse_down_pos): continue
                    self.buttons_pressed.append(button)
            case MouseState.DRAGGING:
                for i in range(len(self.buttons_pressed) - 1, -1, -1):
                    button = self.buttons_pressed[i]
                    if not button.interactable:
                        self.buttons_pressed.pop(i)
                        continue
                    if not button.rect.collidepoint(context.input.mouse_pos):
                        self.buttons_pressed.pop(i)
                        continue
            case MouseState.UP:
                for button in self.buttons_pressed:
                    if not button.interactable: continue
                    if not button.rect.collidepoint(context.input.mouse_up_pos): continue
                    button.on_interact()


    def render(self, context: RenderContext):
        for button in self.buttons:
            button.draw_positioned(context.surface)


    def exit_scope(self):
        pass

    def dispose(self):
        pass