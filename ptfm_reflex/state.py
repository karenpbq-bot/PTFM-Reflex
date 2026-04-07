import reflex as rx
from .base_datos import conectar

class State(rx.State):
    pendientes_rojos: set[str] = set() # Aquí viven los checks rojos (memoria)
    
    def seleccionar_check(self, id_con_hito: str):
        # Esto cambia el color al instante en el navegador
        if id_con_hito in self.pendientes_rojos:
            self.pendientes_rojos.remove(id_con_hito)
        else:
            self.pendientes_rojos.add(id_con_hito)

    def guardar_avances(self):
        # Solo aquí la app conecta con Supabase
        # (Aquí va tu lógica de upsert de base_datos.py)
        self.pendientes_rojos.clear() # Al terminar, se vuelven grises
        return rx.window_alert("¡Guardado en la Nube!")
