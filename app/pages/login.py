import reflex as rx
from app.states.login_state import LoginState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("box", class_name="h-12 w-12 text-blue-600 mx-auto mb-4"),
                rx.el.h2(
                    "PRACTIFORMAS",
                    class_name="text-2xl font-bold text-center text-gray-900",
                ),
                rx.el.p(
                    "Seguimiento y Control de Proyecto",
                    class_name="text-center text-gray-500 mb-8",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Usuario",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="username",
                            placeholder="Ej: admin",
                            required=True,
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Contraseña",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="password",
                            type="password",
                            placeholder="••••••••",
                            required=True,
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                        ),
                        class_name="mb-6",
                    ),
                    rx.cond(
                        LoginState.error_message != "",
                        rx.el.p(
                            LoginState.error_message,
                            class_name="text-red-500 text-sm mb-4 text-center font-medium",
                        ),
                        rx.el.p("", class_name="hidden"),
                    ),
                    rx.el.button(
                        "Iniciar Sesión",
                        type="submit",
                        class_name="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors",
                    ),
                    on_submit=LoginState.login,
                    reset_on_submit=False,
                ),
                class_name="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md border border-gray-100",
            ),
            class_name="flex items-center justify-center min-h-screen w-full",
        ),
        class_name="min-h-screen bg-gray-50 font-['Inter']",
    )