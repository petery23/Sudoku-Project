from engine.contexts import UpdateContext, RenderContext, SceneChangeContext, SceneChangeContext


class System:
    def enter_scope(self, context: SceneChangeContext):
        pass

    def update(self, context: UpdateContext):
        pass

    def render(self, context: RenderContext):
        pass

    def exit_scope(self, context: SceneChangeContext):
        pass

    def dispose(self):
        pass
