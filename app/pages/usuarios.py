import reflex as rx
from app.components.navigation import layout
from app.states.usuarios_state import UsuariosState, UserData
from app.states.login_state import LoginState


def section_title(title: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-5 w-5 text-blue-600"),
        rx.el.h3(title, class_name="text-lg font-bold text-gray-900"),
        class_name="flex items-center gap-2 mb-6 border-b border-gray-100 pb-2",
    )


def user_card(user: UserData) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={user['nombre_usuario']}",
                class_name="size-12 rounded-full bg-gray-100",
            ),
            rx.el.div(
                rx.el.p(
                    user["nombre_completo"],
                    class_name="text-base font-bold text-gray-900",
                ),
                rx.el.p(
                    f"@{user['nombre_usuario']}", class_name="text-sm text-gray-500"
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(
            rx.el.span(
                user["rol"],
                class_name="px-2 py-1 rounded-md text-[10px] font-bold uppercase bg-blue-50 text-blue-600 w-fit",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=lambda: UsuariosState.start_edit(user),
                    class_name="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: UsuariosState.delete_user(user["id"]),
                    class_name="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                ),
                class_name="flex gap-1",
            ),
            class_name="flex justify-between items-center mt-4 pt-4 border-t border-gray-50",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm",
    )


def edit_modal() -> rx.Component:
    return rx.cond(
        UsuariosState.show_edit_modal,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Editar Usuario", class_name="text-xl font-bold text-gray-900"
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-5 w-5"),
                        on_click=UsuariosState.cancel_edit,
                        class_name="text-gray-400 hover:text-gray-600",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Nombre Completo",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="nombre_completo",
                            default_value=UsuariosState.edit_user_name,
                            class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Usuario (Login)",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="nombre_usuario",
                            default_value=UsuariosState.edit_user_username,
                            class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Rol",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.div(
                            rx.el.select(
                                rx.el.option("admin", value="admin"),
                                rx.el.option("Gerente", value="Gerente"),
                                rx.el.option("Supervisor", value="Supervisor"),
                                name="rol",
                                value=UsuariosState.edit_user_role,
                                on_change=UsuariosState.set_edit_user_role,
                                class_name="appearance-none w-full px-4 py-2 border border-gray-200 rounded-xl bg-white focus:ring-2 focus:ring-blue-500",
                            ),
                            rx.icon(
                                "chevron-down",
                                class_name="absolute right-3 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                            ),
                            class_name="relative",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            type="button",
                            on_click=UsuariosState.cancel_edit,
                            class_name="px-4 py-2 text-gray-700 font-medium hover:bg-gray-100 rounded-xl transition-colors",
                        ),
                        rx.el.button(
                            "Guardar Cambios",
                            type="submit",
                            class_name="px-4 py-2 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-colors",
                        ),
                        class_name="flex justify-end gap-3",
                    ),
                    on_submit=UsuariosState.update_user,
                ),
                class_name="bg-white p-8 rounded-2xl w-full max-w-md shadow-2xl",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/40 backdrop-blur-sm p-4",
        ),
        rx.fragment(),
    )


def usuarios_page() -> rx.Component:
    return layout(
        rx.el.div(
            edit_modal(),
            rx.el.div(
                rx.el.div(
                    section_title("Mi Perfil", "circle_user_round"),
                    rx.el.div(
                        rx.image(
                            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={LoginState.user_full_name}",
                            class_name="size-20 rounded-full bg-blue-50 mx-auto mb-4",
                        ),
                        rx.el.p(
                            LoginState.user_full_name,
                            class_name="text-xl font-bold text-center text-gray-900",
                        ),
                        rx.el.p(
                            LoginState.user_role,
                            class_name="text-sm text-center text-gray-500 mb-6 uppercase tracking-wider font-bold",
                        ),
                        rx.el.div(
                            rx.icon("id-card", class_name="h-4 w-4 text-gray-400"),
                            rx.el.span(
                                f"ID del Sistema: {LoginState.user_id}",
                                class_name="text-sm text-gray-600 font-medium",
                            ),
                            class_name="flex items-center gap-2 justify-center",
                        ),
                        class_name="p-6",
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm",
                ),
                rx.el.div(
                    section_title("Cambiar Contraseña", "lock"),
                    rx.el.form(
                        rx.el.div(
                            rx.el.input(
                                name="current_password",
                                type="password",
                                placeholder="Contraseña Actual",
                                class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 mb-3 text-sm",
                            ),
                            rx.el.input(
                                name="new_password",
                                type="password",
                                placeholder="Nueva Contraseña",
                                class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 mb-3 text-sm",
                            ),
                            rx.el.input(
                                name="confirm_password",
                                type="password",
                                placeholder="Confirmar Nueva Contraseña",
                                class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 mb-4 text-sm",
                            ),
                            rx.cond(
                                UsuariosState.password_error != "",
                                rx.el.p(
                                    UsuariosState.password_error,
                                    class_name="text-red-500 text-xs mb-3 font-bold",
                                ),
                                rx.fragment(),
                            ),
                            rx.cond(
                                UsuariosState.password_success != "",
                                rx.el.p(
                                    UsuariosState.password_success,
                                    class_name="text-green-500 text-xs mb-3 font-bold",
                                ),
                                rx.fragment(),
                            ),
                            rx.el.button(
                                "Actualizar Seguridad",
                                type="submit",
                                class_name="w-full bg-gray-900 text-white font-bold py-2 rounded-xl hover:bg-black transition-colors text-sm",
                            ),
                            class_name="flex flex-col",
                        ),
                        on_submit=UsuariosState.change_password,
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8",
            ),
            rx.cond(
                (LoginState.user_role.lower() == "admin")
                | (LoginState.user_role.lower() == "administrador"),
                rx.el.div(
                    section_title("Registrar Colaborador", "user-plus"),
                    rx.el.form(
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Nombre Completo",
                                    class_name="text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.input(
                                    name="nombre_completo",
                                    placeholder="Ej: Juan Pérez",
                                    class_name="w-full px-4 py-2 border border-gray-100 bg-gray-50 rounded-xl focus:ring-2 focus:ring-blue-500 mt-1",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Login Usuario",
                                    class_name="text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.input(
                                    name="nombre_usuario",
                                    placeholder="Ej: jperez",
                                    class_name="w-full px-4 py-2 border border-gray-100 bg-gray-50 rounded-xl focus:ring-2 focus:ring-blue-500 mt-1",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Contraseña Temporal",
                                    class_name="text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.input(
                                    name="contrasena",
                                    type="password",
                                    placeholder="••••••••",
                                    class_name="w-full px-4 py-2 border border-gray-100 bg-gray-50 rounded-xl focus:ring-2 focus:ring-blue-500 mt-1",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Rol / Permisos",
                                    class_name="text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.div(
                                    rx.el.select(
                                        rx.el.option("Supervisor", value="Supervisor"),
                                        rx.el.option("Gerente", value="Gerente"),
                                        rx.el.option("admin", value="admin"),
                                        name="rol",
                                        class_name="appearance-none w-full px-4 py-2 border border-gray-100 bg-gray-50 rounded-xl focus:ring-2 focus:ring-blue-500 mt-1",
                                    ),
                                    rx.icon(
                                        "chevron-down",
                                        class_name="absolute right-3 top-4 h-4 w-4 text-gray-400 pointer-events-none",
                                    ),
                                    class_name="relative",
                                ),
                            ),
                            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4",
                        ),
                        rx.cond(
                            UsuariosState.create_error != "",
                            rx.el.p(
                                UsuariosState.create_error,
                                class_name="text-red-500 text-xs mb-4 font-bold",
                            ),
                            rx.fragment(),
                        ),
                        rx.cond(
                            UsuariosState.create_success != "",
                            rx.el.p(
                                UsuariosState.create_success,
                                class_name="text-green-500 text-xs mb-4 font-bold",
                            ),
                            rx.fragment(),
                        ),
                        rx.el.button(
                            "Crear Usuario",
                            type="submit",
                            class_name="w-full sm:w-fit px-8 py-2 bg-blue-600 text-white font-black rounded-xl hover:bg-blue-700 transition-all shadow-sm",
                        ),
                        on_submit=UsuariosState.create_user,
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm mb-8",
                ),
            ),
            rx.el.div(
                section_title("Equipo Practiformas", "users"),
                rx.el.div(
                    rx.foreach(UsuariosState.users, user_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                class_name="mb-8",
            ),
            class_name="max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700",
        ),
        "Gestión de Usuarios",
    )