import reflex as rx
from typing import TypedDict, Any
from app.services.base_datos import conectar, eliminar_usuario_bd, actualizar_usuario_bd
import logging


class UserData(TypedDict):
    id: int
    nombre_completo: str
    nombre_usuario: str
    rol: str


class UsuariosState(rx.State):
    users: list[UserData] = []
    create_error: str = ""
    create_success: str = ""
    edit_user_id: int = 0
    edit_user_name: str = ""
    edit_user_username: str = ""
    edit_user_role: str = ""
    show_edit_modal: bool = False
    password_error: str = ""
    password_success: str = ""

    @rx.event
    def load_users(self):
        try:
            supabase = conectar()
            if not supabase:
                return
            res = (
                supabase.table("usuarios")
                .select("id, nombre_completo, nombre_usuario, rol")
                .execute()
            )
            self.users = res.data if res.data else []
        except Exception as e:
            logging.exception(f"Error loading users: {e}")
            self.users = []

    @rx.event
    def create_user(self, form_data: dict[str, str]):
        self.create_error = ""
        self.create_success = ""
        try:
            supabase = conectar()
            if not supabase:
                self.create_error = "No hay conexión con la base de datos."
                return
            nombre_completo = form_data.get("nombre_completo", "")
            nombre_usuario = form_data.get("nombre_usuario", "")
            contrasena = form_data.get("contrasena", "")
            rol = form_data.get("rol", "")
            if not (nombre_completo and nombre_usuario and contrasena and rol):
                self.create_error = "Todos los campos son obligatorios."
                return
            data = {
                "nombre_completo": nombre_completo,
                "nombre_usuario": nombre_usuario,
                "contrasena": contrasena,
                "rol": rol,
            }
            supabase.table("usuarios").insert(data).execute()
            self.create_success = f"Usuario {nombre_usuario} creado exitosamente."
            yield UsuariosState.load_users
        except Exception as e:
            logging.exception(f"Error creating user: {e}")
            self.create_error = (
                "Error al crear el usuario. El nombre de usuario podría ya existir."
            )

    @rx.event
    def delete_user(self, user_id: int):
        try:
            eliminar_usuario_bd(user_id)
            yield UsuariosState.load_users
        except Exception as e:
            logging.exception(f"Error deleting user: {e}")

    @rx.event
    def start_edit(self, user: UserData):
        self.edit_user_id = user["id"]
        self.edit_user_name = user["nombre_completo"]
        self.edit_user_username = user["nombre_usuario"]
        self.edit_user_role = user["rol"]
        self.show_edit_modal = True

    @rx.event
    def cancel_edit(self):
        self.show_edit_modal = False

    @rx.event
    def update_user(self, form_data: dict[str, str]):
        try:
            data = {
                "nombre_completo": form_data.get("nombre_completo", ""),
                "nombre_usuario": form_data.get("nombre_usuario", ""),
                "rol": form_data.get("rol", ""),
            }
            actualizar_usuario_bd(self.edit_user_id, data)
            self.show_edit_modal = False
            yield UsuariosState.load_users
        except Exception as e:
            logging.exception(f"Error updating user: {e}")

    @rx.event
    async def change_password(self, form_data: dict[str, str]):
        from app.states.login_state import LoginState

        login_state = await self.get_state(LoginState)
        self.password_error = ""
        self.password_success = ""
        current_pwd = form_data.get("current_password", "")
        new_pwd = form_data.get("new_password", "")
        confirm_pwd = form_data.get("confirm_password", "")
        if not (current_pwd and new_pwd and confirm_pwd):
            self.password_error = "Todos los campos son obligatorios."
            return
        if new_pwd != confirm_pwd:
            self.password_error = "La nueva contraseña no coincide."
            return
        try:
            supabase = conectar()
            res = (
                supabase.table("usuarios")
                .select("contrasena")
                .eq("id", login_state.user_id)
                .execute()
            )
            if res.data and res.data[0]["contrasena"] == current_pwd:
                supabase.table("usuarios").update({"contrasena": new_pwd}).eq(
                    "id", login_state.user_id
                ).execute()
                self.password_success = "Contraseña actualizada correctamente."
            else:
                self.password_error = "La contraseña actual es incorrecta."
        except Exception as e:
            logging.exception(f"Error changing password: {e}")
            self.password_error = "Error al actualizar la contraseña."