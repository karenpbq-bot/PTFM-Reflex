import reflex as rx
from typing import TypedDict
from app.services.base_datos import conectar
from app.states.login_state import LoginState
from datetime import datetime
import logging


class ProjectSelectorItem(TypedDict):
    id: str
    label: str
    codigo: str


class TmpPieza(TypedDict):
    descripcion: str
    cantidad: int
    ubicacion: str
    material: str
    rotacion: int
    veta: float
    no_veta: float
    tc_f: str
    tc_p: str
    tc_d: str
    tc_i: str


class TmpMaterial(TypedDict):
    descripcion: str
    cantidad: int
    observaciones: str


class IncidenciaHistorialItem(TypedDict):
    id: int
    proyecto_label: str
    tipo_requerimiento: str
    categoria: str
    estado: str
    created_at: str
    detalles: list[dict[str, str | int | float]]
    fecha_almacen: str
    fecha_solicitante: str
    fecha_teowin: str
    obs_gestion: str
    has_almacen: bool
    has_solicitante: bool
    has_teowin: bool
    supervisor_id: int


class IncidenciasState(rx.State):
    projects_list: list[ProjectSelectorItem] = []
    search_project_text: str = ""
    selected_project_id: str = ""
    selected_project_label: str = ""
    tipo_requerimiento: str = "Piezas"
    categoria: str = "Faltante"
    pz_descripcion: str = ""
    pz_cantidad: int = 1
    pz_ubicacion: str = ""
    pz_material: str = ""
    pz_rotacion: int = 1
    pz_veta: float = 0.0
    pz_no_veta: float = 0.0
    pz_tc_f: str = ""
    pz_tc_p: str = ""
    pz_tc_d: str = ""
    pz_tc_i: str = ""
    mat_descripcion: str = ""
    mat_cantidad: int = 1
    mat_observaciones: str = ""
    tmp_piezas: list[TmpPieza] = []
    tmp_materiales: list[TmpMaterial] = []
    historial: list[IncidenciaHistorialItem] = []
    expanded_ids: list[int] = []
    reg_message: str = ""
    reg_error: str = ""

    @rx.var
    def filtered_projects(self) -> list[ProjectSelectorItem]:
        if not self.search_project_text:
            return self.projects_list
        return [
            p
            for p in self.projects_list
            if self.search_project_text.lower() in p["label"].lower()
        ]

    @rx.var
    def show_piezas_form(self) -> bool:
        return self.tipo_requerimiento == "Piezas"

    @rx.event
    async def load_incidencias(self):
        try:
            from app.states.login_state import LoginState

            login_state = await self.get_state(LoginState)
            user_role = login_state.user_role
            user_id = str(login_state.user_id)
            supabase = conectar()
            if not supabase:
                return
            res_proj = (
                supabase.table("proyectos")
                .select("id, codigo, proyecto_text, supervisor_id")
                .order("created_at", desc=True)
                .execute()
            )
            if res_proj.data:
                all_p = res_proj.data
                if user_role == "Supervisor":
                    all_p = [
                        p for p in all_p if str(p.get("supervisor_id", "")) == user_id
                    ]
                self.projects_list = [
                    {
                        "id": str(p["id"]),
                        "codigo": str(p["codigo"]),
                        "label": f"[{p['codigo']}] {p['proyecto_text']}",
                    }
                    for p in all_p
                ]
            res_inc = (
                supabase.table("incidencias")
                .select("*, proyectos(codigo, proyecto_text)")
                .order("created_at", desc=True)
                .execute()
            )
            if res_inc.data:
                loaded: list[IncidenciaHistorialItem] = []
                for r in res_inc.data:
                    proj = r.get("proyectos")
                    p_label = (
                        f"[{proj['codigo']}] {proj['proyecto_text']}"
                        if proj
                        else "Sin Proyecto"
                    )
                    dt_str = r.get("created_at", "")
                    if dt_str:
                        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
                        dt_formatted = dt.strftime("%d/%m/%Y %H:%M")
                    else:
                        dt_formatted = ""
                    f_alm = r.get("fecha_almacen")
                    f_sol = r.get("fecha_solicitante")
                    f_teo = r.get("fecha_teowin")
                    det = r.get("detalles")
                    if not isinstance(det, list):
                        det = []
                    loaded.append(
                        {
                            "id": int(r["id"]),
                            "proyecto_label": p_label,
                            "tipo_requerimiento": str(r.get("tipo_requerimiento", "")),
                            "categoria": str(r.get("categoria", "")),
                            "estado": str(r.get("estado", "Pendiente")),
                            "created_at": dt_formatted,
                            "detalles": det,
                            "fecha_almacen": str(f_alm) if f_alm else "",
                            "fecha_solicitante": str(f_sol) if f_sol else "",
                            "fecha_teowin": str(f_teo) if f_teo else "",
                            "obs_gestion": str(r.get("obs_gestion", "")),
                            "has_almacen": bool(f_alm),
                            "has_solicitante": bool(f_sol),
                            "has_teowin": bool(f_teo),
                            "supervisor_id": int(r.get("supervisor_id", 0) or 0),
                        }
                    )
                self.historial = loaded
            else:
                self.historial = []
        except Exception as e:
            logging.exception(f"Error in load_incidencias: {e}")

    @rx.event
    def set_search_project_text(self, val: str):
        self.search_project_text = val

    @rx.event
    def select_project_registro(self, project_id: str):
        self.selected_project_id = project_id
        for p in self.projects_list:
            if p["id"] == project_id:
                self.selected_project_label = p["label"]
                break

    @rx.event
    def set_tipo_requerimiento(self, val: str):
        self.tipo_requerimiento = val
        self.tmp_piezas = []
        self.tmp_materiales = []
        self.reg_error = ""
        self.reg_message = ""

    @rx.event
    def add_pieza_to_matrix(self):
        if not self.pz_descripcion:
            self.reg_error = "La descripción de la pieza es obligatoria."
            return
        self.tmp_piezas.append(
            {
                "descripcion": self.pz_descripcion,
                "cantidad": self.pz_cantidad,
                "ubicacion": self.pz_ubicacion,
                "material": self.pz_material,
                "rotacion": self.pz_rotacion,
                "veta": self.pz_veta,
                "no_veta": self.pz_no_veta,
                "tc_f": self.pz_tc_f,
                "tc_p": self.pz_tc_p,
                "tc_d": self.pz_tc_d,
                "tc_i": self.pz_tc_i,
            }
        )
        self.pz_descripcion = ""
        self.pz_cantidad = 1
        self.pz_ubicacion = ""
        self.pz_material = ""
        self.pz_rotacion = 1
        self.pz_veta = 0.0
        self.pz_no_veta = 0.0
        self.pz_tc_f = ""
        self.pz_tc_p = ""
        self.pz_tc_d = ""
        self.pz_tc_i = ""
        self.reg_error = ""

    @rx.event
    def remove_pieza(self, idx: int):
        if 0 <= idx < len(self.tmp_piezas):
            self.tmp_piezas.pop(idx)

    @rx.event
    def add_material_to_matrix(self):
        if not self.mat_descripcion:
            self.reg_error = "La descripción del material es obligatoria."
            return
        self.tmp_materiales.append(
            {
                "descripcion": self.mat_descripcion,
                "cantidad": self.mat_cantidad,
                "observaciones": self.mat_observaciones,
            }
        )
        self.mat_descripcion = ""
        self.mat_cantidad = 1
        self.mat_observaciones = ""
        self.reg_error = ""

    @rx.event
    def remove_material(self, idx: int):
        if 0 <= idx < len(self.tmp_materiales):
            self.tmp_materiales.pop(idx)

    @rx.event
    async def enviar_requerimiento(self):
        self.reg_error = ""
        self.reg_message = ""
        if not self.selected_project_id:
            self.reg_error = "Debe seleccionar un proyecto."
            return
        if self.tipo_requerimiento == "Piezas" and (not self.tmp_piezas):
            self.reg_error = "Agregue al menos una pieza a la matriz."
            return
        if self.tipo_requerimiento == "Materiales" and (not self.tmp_materiales):
            self.reg_error = "Agregue al menos un material a la matriz."
            return
        login_state = await self.get_state(LoginState)
        try:
            supabase = conectar()
            if not supabase:
                self.reg_error = "Error de conexión a la base de datos."
                return
            detalles = (
                self.tmp_piezas
                if self.tipo_requerimiento == "Piezas"
                else self.tmp_materiales
            )
            data = {
                "proyecto_id": int(self.selected_project_id),
                "supervisor_id": login_state.user_id,
                "tipo_requerimiento": self.tipo_requerimiento,
                "categoria": self.categoria,
                "detalles": detalles,
                "estado": "Pendiente",
            }
            supabase.table("incidencias").insert(data).execute()
            self.tmp_piezas = []
            self.tmp_materiales = []
            self.selected_project_id = ""
            self.selected_project_label = ""
            self.reg_message = "Requerimiento enviado exitosamente."
            yield IncidenciasState.load_incidencias
        except Exception as e:
            logging.exception(f"Error al enviar requerimiento: {e}")
            self.reg_error = "Ocurrió un error al enviar el requerimiento."

    @rx.event
    def toggle_accordion(self, inc_id: int):
        if inc_id in self.expanded_ids:
            self.expanded_ids.remove(inc_id)
        else:
            self.expanded_ids.append(inc_id)

    @rx.event
    def toggle_fecha_field(self, inc_id: int, field: str):
        try:
            supabase = conectar()
            if not supabase:
                return
            item = next((i for i in self.historial if i["id"] == inc_id), None)
            if not item:
                return
            current_val = item[field]
            new_val = None if current_val else datetime.now().strftime("%d/%m/%Y %H:%M")
            supabase.table("incidencias").update({field: new_val}).eq(
                "id", inc_id
            ).execute()
            for i in range(len(self.historial)):
                if self.historial[i]["id"] == inc_id:
                    self.historial[i][field] = new_val if new_val else ""
                    if field == "fecha_almacen":
                        self.historial[i]["has_almacen"] = bool(new_val)
                    elif field == "fecha_solicitante":
                        self.historial[i]["has_solicitante"] = bool(new_val)
                    elif field == "fecha_teowin":
                        self.historial[i]["has_teowin"] = bool(new_val)
                    break
        except Exception as e:
            logging.exception(f"Error toggling fecha: {e}")

    @rx.event
    def update_obs_gestion(self, inc_id: int, value: str):
        try:
            supabase = conectar()
            if not supabase:
                return
            supabase.table("incidencias").update({"obs_gestion": value}).eq(
                "id", inc_id
            ).execute()
            for i in range(len(self.historial)):
                if self.historial[i]["id"] == inc_id:
                    self.historial[i]["obs_gestion"] = value
                    break
        except Exception as e:
            logging.exception(f"Error updating obs_gestion: {e}")