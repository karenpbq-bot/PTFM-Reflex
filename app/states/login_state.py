import reflex as rx
from app.services.base_datos import validar_usuario
import logging


class LoginState(rx.State):
    username: str = ""
    password: str = ""
    show_password: bool = False
    is_authenticated: bool = False
    user_role: str = ""
    user_id: int = 0
    user_full_name: str = ""
    error_message: str = ""

    @rx.event
    def toggle_password_visibility(self):
        self.show_password = not self.show_password

    @rx.event
    def login(self, form_data: dict):
        try:
            user = form_data.get("username", "")
            pwd = form_data.get("password", "")
            res = validar_usuario(user, pwd)
            if res:
                self.is_authenticated = True
                self.user_role = res.get("rol", "")
                self.user_id = res.get("id", 0)
                self.user_full_name = res.get(
                    "nombre_completo", res.get("nombre_usuario", "")
                )
                self.error_message = ""
                return rx.redirect("/")
            else:
                self.error_message = "Usuario o contraseña incorrectos."
        except Exception as e:
            logging.exception(f"Error al iniciar sesión: {e}")
            self.error_message = "Error del servidor al intentar iniciar sesión."

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.user_role = ""
        self.user_id = 0
        self.user_full_name = ""
        self.username = ""
        self.password = ""
        return rx.redirect("/login")

    @rx.var
    def check_auth(self) -> bool:
        return self.is_authenticated