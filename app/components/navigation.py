import reflex as rx
from app.states.navigation_state import SidebarState
from app.states.login_state import LoginState


def nav_item(label: str, icon: str, href: str) -> rx.Component:
    is_active = SidebarState.current_route == href
    return rx.el.a(
        rx.icon(icon, class_name="h-5 w-5 shrink-0"),
        rx.el.span(
            label,
            class_name=rx.cond(
                SidebarState.sidebar_visible,
                "ml-3 whitespace-nowrap overflow-hidden",
                "hidden",
            ),
        ),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center p-3 rounded-lg bg-blue-50 text-blue-600 transition-colors duration-200 border-l-4 border-blue-600",
            "flex items-center p-3 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors duration-200 border-l-4 border-transparent",
        ),
    )


def sidebar() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            on_click=SidebarState.toggle_sidebar,
            class_name=rx.cond(
                SidebarState.sidebar_visible,
                "fixed inset-0 bg-gray-900/50 z-40 lg:hidden",
                "hidden",
            ),
        ),
        rx.el.aside(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("box", class_name="h-8 w-8 text-blue-600"),
                        rx.el.span(
                            "PTFM", class_name="ml-2 text-2xl font-bold text-gray-900"
                        ),
                        class_name=rx.cond(
                            SidebarState.sidebar_visible,
                            "flex items-center px-4 py-6 border-b border-gray-100",
                            "hidden",
                        ),
                    ),
                    class_name="h-20",
                ),
                rx.cond(
                    SidebarState.sidebar_visible & (LoginState.user_full_name != ""),
                    rx.el.div(
                        rx.icon(
                            "circle-user-round",
                            class_name="h-8 w-8 text-gray-400 shrink-0",
                        ),
                        rx.el.div(
                            rx.el.p(
                                LoginState.user_full_name,
                                class_name="text-sm font-bold text-gray-900 leading-tight truncate",
                            ),
                            rx.el.p(
                                LoginState.user_role,
                                class_name="text-xs text-gray-500 font-medium truncate",
                            ),
                            class_name="flex flex-col min-w-0",
                        ),
                        class_name="flex items-center gap-3 px-4 py-3 border-b border-gray-100 animate-in fade-in duration-300",
                    ),
                    None,
                ),
                rx.el.nav(
                    rx.el.div(
                        nav_item("Proyectos", "folder-kanban", "/proyectos"),
                        nav_item("Seguimiento", "map", "/seguimiento"),
                        nav_item("Métricas", "bar-chart-3", "/metricas"),
                        nav_item("Incidencias", "circle_alert", "/incidencias"),
                        nav_item("Usuarios", "users", "/usuarios"),
                        class_name="flex flex-col gap-2 p-4",
                    ),
                    class_name="flex-1 overflow-y-auto",
                ),
                rx.el.div(
                    rx.el.div(class_name="border-t border-gray-100 mx-4"),
                    rx.el.button(
                        rx.icon("log-out", class_name="h-5 w-5 shrink-0"),
                        rx.el.span(
                            "Cerrar Sesión",
                            class_name=rx.cond(
                                SidebarState.sidebar_visible,
                                "ml-3 whitespace-nowrap overflow-hidden",
                                "hidden",
                            ),
                        ),
                        on_click=LoginState.logout,
                        class_name="flex items-center w-full p-3 rounded-lg text-red-500 hover:bg-red-50 transition-colors duration-200 mt-2",
                    ),
                    class_name="p-4",
                ),
                class_name="flex flex-col h-full bg-white border-r border-gray-200",
            ),
            class_name=rx.cond(
                SidebarState.sidebar_visible,
                "fixed inset-y-0 left-0 z-50 w-64 transition-all duration-300 ease-in-out transform translate-x-0 shadow-lg lg:shadow-none",
                "fixed inset-y-0 left-0 z-50 w-0 transition-all duration-300 ease-in-out transform -translate-x-full lg:translate-x-0",
            ),
        ),
    )


def layout(content: rx.Component, title: str) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            rx.el.header(
                rx.el.div(
                    rx.el.button(
                        rx.icon("menu", class_name="h-6 w-6"),
                        on_click=SidebarState.toggle_sidebar,
                        class_name="p-2 rounded-lg text-gray-500 hover:bg-gray-100 focus:outline-none transition-colors",
                    ),
                    rx.el.h1(
                        title, class_name="ml-4 text-xl font-semibold text-gray-800"
                    ),
                    class_name="flex items-center h-16 px-4",
                ),
                class_name="fixed top-0 right-0 left-0 z-30 bg-white/80 backdrop-blur-md border-b border-gray-200 transition-all duration-300",
                style={
                    "paddingLeft": rx.cond(SidebarState.sidebar_visible, "16rem", "0px")
                },
            ),
            rx.el.main(
                rx.el.div(content, class_name="mt-16 p-6"),
                class_name="min-h-screen transition-all duration-300",
                style={
                    "paddingLeft": rx.cond(SidebarState.sidebar_visible, "16rem", "0px")
                },
            ),
            class_name="flex-1 flex flex-col min-h-screen bg-gray-50",
        ),
        class_name="flex min-h-screen font-['Inter']",
    )