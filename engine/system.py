from engine.engine import UpdateContext, RenderContext

class System:
    def enter_scope(self):
        pass

    def update(self, context: UpdateContext):
        pass

    def render(self, context: RenderContext):
        pass

    def exit_scope(self):
        pass

    def dispose(self):
        pass
