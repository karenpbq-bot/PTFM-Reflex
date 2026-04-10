import reflex as rx
from app.states.login_state import LoginState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("box", class_name="h-16 w-16 text-blue-600 mb-2"),
                    class_name="flex justify-center mb-4 animate-bounce",
                ),
                rx.el.h2(
                    "PRACTIFORMAS",
                    class_name="text-3xl font-black text-center text-gray-900 tracking-tight",
                ),
                rx.el.p(
                    "Seguimiento y Control de Proyecto",
                    class_name="text-center text-gray-500 mb-10 font-medium",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Nombre de Usuario",
                            class_name="block text-xs font-bold text-gray-400 uppercase mb-1 ml-1",
                        ),
                        rx.el.div(
                            rx.icon(
                                "user",
                                class_name="absolute left-3 top-3 h-4 w-4 text-gray-400",
                            ),
                            rx.el.input(
                                name="username",
                                placeholder="Ej: Kbarrientos",
                                required=True,
                                class_name="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all outline-none bg-gray-50/50",
                            ),
                            class_name="relative",
                        ),
                        class_name="mb-5",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Contraseña",
                            class_name="block text-xs font-bold text-gray-400 uppercase mb-1 ml-1",
                        ),
                        rx.el.div(
                            rx.icon(
                                "lock",
                                class_name="absolute left-3 top-3 h-4 w-4 text-gray-400",
                            ),
                            rx.el.input(
                                name="password",
                                type=rx.cond(
                                    LoginState.show_password, "text", "password"
                                ),
                                placeholder="••••••••",
                                required=True,
                                class_name="w-full pl-10 pr-12 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all outline-none bg-gray-50/50",
                            ),
                            rx.el.button(
                                rx.cond(
                                    LoginState.show_password,
                                    rx.icon("eye-off", class_name="h-5 w-5"),
                                    rx.icon("eye", class_name="h-5 w-5"),
                                ),
                                on_click=LoginState.toggle_password_visibility,
                                type="button",
                                class_name="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-gray-400 hover:text-blue-600 focus:outline-none transition-colors",
                            ),
                            class_name="relative",
                        ),
                        class_name="mb-8",
                    ),
                    rx.cond(
                        LoginState.error_message != "",
                        rx.el.div(
                            rx.icon("circle-alert", class_name="h-4 w-4"),
                            rx.el.p(
                                LoginState.error_message, class_name="text-sm font-bold"
                            ),
                            class_name="flex items-center gap-2 bg-red-50 text-red-500 p-3 rounded-xl mb-6 border border-red-100",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.button(
                        "Ingresar al Sistema",
                        type="submit",
                        disabled=LoginState.is_loading,
                        class_name="w-full bg-blue-600 text-white font-black py-3 px-4 rounded-xl hover:bg-blue-700 transition-all shadow-lg hover:shadow-blue-200 disabled:opacity-50 transition-all duration-200",
                    ),
                    rx.cond(
                        LoginState.is_loading,
                        rx.el.div(
                            rx.icon(
                                "loader",
                                class_name="h-4 w-4 animate-spin text-blue-600",
                            ),
                            rx.el.span(
                                "Verificando credenciales...",
                                class_name="text-xs font-bold text-blue-600",
                            ),
                            class_name="flex items-center justify-center gap-2 mt-4 animate-pulse",
                        ),
                    ),
                    on_submit=LoginState.login,
                    reset_on_submit=False,
                ),
                rx.el.div(
                    rx.el.p(
                        "v2.1.0",
                        class_name="text-[10px] text-gray-300 font-bold uppercase tracking-widest mt-12 text-center",
                    )
                ),
                class_name="bg-white p-10 rounded-3xl shadow-2xl w-full max-w-md border border-gray-100 transform transition-all duration-500 hover:scale-[1.01]",
            ),
            class_name="flex items-center justify-center min-h-screen w-full px-4",
        ),
        class_name="min-h-screen bg-gray-50 font-['Inter'] relative overflow-hidden",
        style={
            "backgroundImage": "radial-gradient(circle at 2px 2px, rgba(0,0,0,0.02) 1px, transparent 0)",
            "backgroundSize": "24px 24px",
        },
    )