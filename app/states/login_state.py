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
    is_loading: bool = False

    @rx.event
    def toggle_password_visibility(self):
        self.show_password = not self.show_password

    @rx.event
    def login(self, form_data: dict):
        """Simplified login handler to prevent React DOM update race conditions during redirect."""
        self.is_loading = True
        self.error_message = ""
        try:
            user = form_data.get("username", "").strip()
            pwd = form_data.get("password", "")
            if not user or not pwd:
                self.error_message = "Por favor ingrese usuario y contraseña."
                self.is_loading = False
                return
            res = validar_usuario(user, pwd)
            if res:
                self.is_authenticated = True
                self.user_role = res.get("rol", "")
                self.user_id = res.get("id", 0)
                self.user_full_name = res.get(
                    "nombre_completo", res.get("nombre_usuario", "")
                )
                self.error_message = ""
                self.is_loading = False
                return rx.redirect("/")
            else:
                self.error_message = (
                    "Credenciales inválidas. Verifique mayúsculas y minúsculas."
                )
                self.is_loading = False
        except Exception as e:
            logging.exception(f"Error al iniciar sesión: {e}")
            self.error_message = "Error del servidor al intentar iniciar sesión."
            self.is_loading = False

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.user_role = ""
        self.user_id = 0
        self.user_full_name = ""
        self.username = ""
        self.password = ""
        self.error_message = ""
        return rx.redirect("/login")

    @rx.var
    def check_auth(self) -> bool:
        return self.is_authenticated