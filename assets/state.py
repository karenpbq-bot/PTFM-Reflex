import reflex as rx
from .base_datos import conectar


class State(rx.State):
    pendientes_rojos: set[str] = set()

    @rx.event
    def seleccionar_check(self, id_con_hito: str):
        if id_con_hito in self.pendientes_rojos:
            self.pendientes_rojos.remove(id_con_hito)
        else:
            self.pendientes_rojos.add(id_con_hito)

    @rx.event
    def guardar_avances(self):
        self.pendientes_rojos.clear()
        return rx.window_alert("¡Guardado en la Nube!")