import reflex as rx


class SidebarState(rx.State):
    sidebar_visible: bool = True

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_visible = not self.sidebar_visible

    @rx.var
    def sidebar_width(self) -> str:
        return "240px" if self.sidebar_visible else "0px"

    @rx.var
    def content_margin(self) -> str:
        return "240px" if self.sidebar_visible else "0px"

    @rx.var
    def current_route(self) -> str:
        return self.router.page.path