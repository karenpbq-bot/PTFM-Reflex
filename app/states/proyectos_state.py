import reflex as rx
from typing import TypedDict, Any
from app.services.base_datos import conectar
from datetime import datetime, timedelta
import pandas as pd
import io
import logging


class SupervisorData(TypedDict):
    id: int
    nombre: str


class ProjectData(TypedDict):
    id: str
    codigo: str
    nombre: str
    cliente: str
    estatus: str
    partida: str
    supervisor_id: int
    f_ini: str
    f_fin: str


class ProductData(TypedDict):
    id: str
    codigo_etiqueta: str
    ubicacion: str
    tipo: str
    ctd: int
    ml: float


class TimelineStage(TypedDict):
    etapa: str
    inicio: str
    fin: str
    dias: int


class ProyectosState(rx.State):
    projects: list[ProjectData] = []
    supervisores: list[SupervisorData] = []
    reg_codigo: str = ""
    reg_nombre: str = ""
    reg_cliente: str = ""
    reg_partida: str = ""
    reg_responsable: str = ""
    reg_f_ini: str = datetime.now().strftime("%Y-%m-%d")
    reg_f_fin: str = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    pct_diseno: int = 15
    pct_fabricacion: int = 40
    pct_traslado: int = 10
    pct_instalacion: int = 25
    pct_entrega: int = 10
    reg_message: str = ""
    reg_error: str = ""
    sel_proj_tab2: str = ""
    products_tab2: list[ProductData] = []
    prod_ubicacion: str = ""
    prod_tipo: str = ""
    prod_ctd: int = 1
    prod_ml: float = 0.0
    matriz_message: str = ""
    matriz_error: str = ""
    sel_proj_tab3: str = ""
    edit_nombre: str = ""
    edit_cliente: str = ""
    edit_partida: str = ""
    edit_responsable: str = ""
    edit_estatus: str = ""
    edit_message: str = ""
    edit_error: str = ""

    @rx.var
    def total_pct(self) -> int:
        return (
            self.pct_diseno
            + self.pct_fabricacion
            + self.pct_traslado
            + self.pct_instalacion
            + self.pct_entrega
        )

    @rx.var
    def is_pct_valid(self) -> bool:
        return self.total_pct == 100

    @rx.var
    def calculated_timeline(self) -> list[TimelineStage]:
        if not self.is_pct_valid or not self.reg_f_ini or (not self.reg_f_fin):
            return []
        try:
            f_ini = datetime.strptime(self.reg_f_ini, "%Y-%m-%d")
            f_fin = datetime.strptime(self.reg_f_fin, "%Y-%m-%d")
            total_days = (f_fin - f_ini).days
            if total_days <= 0:
                return []
            stages = [
                ("Diseño", self.pct_diseno),
                ("Fabricación", self.pct_fabricacion),
                ("Traslado", self.pct_traslado),
                ("Instalación", self.pct_instalacion),
                ("Entrega", self.pct_entrega),
            ]
            timeline: list[TimelineStage] = []
            current_date = f_ini
            for nombre_etapa, pct in stages:
                dias = round(total_days * (pct / 100))
                end_date = current_date + timedelta(days=max(0, dias - 1))
                timeline.append(
                    {
                        "etapa": nombre_etapa,
                        "inicio": current_date.strftime("%Y-%m-%d"),
                        "fin": end_date.strftime("%Y-%m-%d"),
                        "dias": dias,
                    }
                )
                current_date = end_date + timedelta(days=1)
            return timeline
        except Exception:
            logging.exception("Unexpected error")
            return []

    @rx.event
    def load_initial_data(self):
        self.load_supervisores()
        self.load_projects()

    @rx.event
    def load_supervisores(self):
        try:
            supabase = conectar()
            if supabase:
                res = (
                    supabase.table("usuarios")
                    .select("id, nombre_completo")
                    .in_("rol", ["admin", "Administrador", "Gerente", "Supervisor"])
                    .execute()
                )
                if res.data:
                    self.supervisores = [
                        {"id": r["id"], "nombre": r["nombre_completo"]}
                        for r in res.data
                    ]
        except Exception as e:
            logging.exception(f"Error loading supervisores: {e}")

    @rx.event
    def load_projects(self):
        try:
            supabase = conectar()
            if supabase:
                res = (
                    supabase.table("proyectos")
                    .select(
                        "id, codigo, proyecto_text, cliente, estatus, partida, supervisor_id, f_ini, f_fin"
                    )
                    .order("created_at", desc=True)
                    .execute()
                )
                if res.data:
                    self.projects = [
                        {
                            "id": str(r["id"]),
                            "codigo": r.get("codigo", ""),
                            "nombre": r.get("proyecto_text", ""),
                            "cliente": r.get("cliente", ""),
                            "estatus": r.get("estatus", "Activo"),
                            "partida": r.get("partida", ""),
                            "supervisor_id": r.get("supervisor_id", 0),
                            "f_ini": r.get("f_ini", ""),
                            "f_fin": r.get("f_fin", ""),
                        }
                        for r in res.data
                    ]
        except Exception as e:
            logging.exception(f"Error loading projects: {e}")

    @rx.event
    def save_project(self):
        self.reg_message = ""
        self.reg_error = ""
        if not self.reg_codigo or not self.reg_nombre:
            self.reg_error = "El código y el nombre son obligatorios."
            return
        if not self.is_pct_valid:
            self.reg_error = "La suma de los porcentajes debe ser exactamente 100%."
            return
        timeline = self.calculated_timeline
        if not timeline:
            self.reg_error = "Fechas inválidas o cronograma no calculable."
            return
        try:
            supabase = conectar()
            if not supabase:
                self.reg_error = "Error de conexión a la base de datos."
                return
            data = {
                "codigo": self.reg_codigo,
                "proyecto_text": self.reg_nombre,
                "cliente": self.reg_cliente,
                "partida": self.reg_partida,
                "supervisor_id": int(self.reg_responsable)
                if self.reg_responsable
                else None,
                "f_ini": self.reg_f_ini,
                "f_fin": self.reg_f_fin,
                "estatus": "Activo",
                "avance": 0,
                "p_dis_i": timeline[0]["inicio"],
                "p_dis_f": timeline[0]["fin"],
                "p_fab_i": timeline[1]["inicio"],
                "p_fab_f": timeline[1]["fin"],
                "p_tra_i": timeline[2]["inicio"],
                "p_tra_f": timeline[2]["fin"],
                "p_ins_i": timeline[3]["inicio"],
                "p_ins_f": timeline[3]["fin"],
                "p_ent_i": timeline[4]["inicio"],
                "p_ent_f": timeline[4]["fin"],
            }
            supabase.table("proyectos").insert(data).execute()
            self.reg_message = f"Proyecto {self.reg_codigo} registrado exitosamente."
            self.reg_codigo = ""
            self.reg_nombre = ""
            self.reg_cliente = ""
            self.reg_partida = ""
            self.load_projects()
        except Exception as e:
            logging.exception(f"Error saving project: {e}")
            self.reg_error = (
                "Error al guardar el proyecto. Puede que el código ya exista."
            )

    @rx.event
    def select_project_tab2(self, project_id: str):
        self.sel_proj_tab2 = project_id
        self.matriz_message = ""
        self.matriz_error = ""
        self.load_products()

    @rx.event
    def load_products(self):
        if not self.sel_proj_tab2:
            self.products_tab2 = []
            return
        try:
            supabase = conectar()
            if supabase:
                res = (
                    supabase.table("productos")
                    .select("*")
                    .eq("proyecto_id", self.sel_proj_tab2)
                    .order("codigo_etiqueta")
                    .execute()
                )
                if res.data:
                    self.products_tab2 = [
                        {
                            "id": str(r["id"]),
                            "codigo_etiqueta": r.get("codigo_etiqueta", ""),
                            "ubicacion": r.get("ubicacion", ""),
                            "tipo": r.get("tipo", ""),
                            "ctd": r.get("ctd", 0),
                            "ml": r.get("ml", 0.0),
                        }
                        for r in res.data
                    ]
                else:
                    self.products_tab2 = []
        except Exception as e:
            logging.exception(f"Error loading products: {e}")
            self.products_tab2 = []

    @rx.var
    def total_products(self) -> int:
        return sum((p["ctd"] for p in self.products_tab2))

    @rx.var
    def total_metraje(self) -> str:
        total = sum((p["ml"] for p in self.products_tab2))
        return f"{total:.2f}"

    @rx.event
    def add_manual_product(self):
        self.matriz_message = ""
        self.matriz_error = ""
        if not self.sel_proj_tab2:
            self.matriz_error = "Seleccione un proyecto primero."
            return
        if not self.prod_ubicacion or not self.prod_tipo:
            self.matriz_error = "Ubicación y Tipo son obligatorios."
            return
        try:
            supabase = conectar()
            if not supabase:
                return
            res_p = (
                supabase.table("proyectos")
                .select("codigo")
                .eq("id", self.sel_proj_tab2)
                .single()
                .execute()
            )
            if not res_p.data:
                return
            p_codigo = res_p.data["codigo"]
            res_c = (
                supabase.table("productos")
                .select("id", count="exact")
                .eq("proyecto_id", self.sel_proj_tab2)
                .execute()
            )
            count = res_c.count if res_c.count else 0
            codigo_etiqueta = f"{p_codigo}-{str(count + 1).zfill(4)}"
            data = {
                "proyecto_id": int(self.sel_proj_tab2),
                "codigo_etiqueta": codigo_etiqueta,
                "ubicacion": self.prod_ubicacion,
                "tipo": self.prod_tipo,
                "ctd": int(self.prod_ctd),
                "ml": float(self.prod_ml),
            }
            supabase.table("productos").insert(data).execute()
            self.matriz_message = f"Producto agregado con código {codigo_etiqueta}."
            self.prod_ubicacion = ""
            self.prod_tipo = ""
            self.prod_ctd = 1
            self.prod_ml = 0.0
            self.load_products()
        except Exception as e:
            logging.exception(f"Error adding manual product: {e}")
            self.matriz_error = "Error al guardar el producto."

    @rx.event
    async def handle_excel_upload(self, files: list[rx.UploadFile]):
        self.matriz_message = ""
        self.matriz_error = ""
        if not self.sel_proj_tab2:
            self.matriz_error = "Seleccione un proyecto primero."
            return
        if not files:
            return
        try:
            file = files[0]
            upload_data = await file.read()
            df = pd.read_excel(io.BytesIO(upload_data))
            required_cols = ["UBICACION", "TIPO", "CTD", "Medidas (ml)"]
            if not all((col in df.columns for col in required_cols)):
                self.matriz_error = "El archivo Excel no tiene las columnas requeridas (UBICACION, TIPO, CTD, Medidas (ml))."
                return
            df = df.dropna(subset=["UBICACION", "TIPO"])
            supabase = conectar()
            if not supabase:
                return
            res_p = (
                supabase.table("proyectos")
                .select("codigo")
                .eq("id", self.sel_proj_tab2)
                .single()
                .execute()
            )
            p_codigo = res_p.data["codigo"]
            res_c = (
                supabase.table("productos")
                .select("id", count="exact")
                .eq("proyecto_id", self.sel_proj_tab2)
                .execute()
            )
            count = res_c.count if res_c.count else 0
            lote = []
            for i, row in df.iterrows():
                count += 1
                codigo_etiqueta = f"{p_codigo}-{str(count).zfill(4)}"
                lote.append(
                    {
                        "proyecto_id": int(self.sel_proj_tab2),
                        "codigo_etiqueta": codigo_etiqueta,
                        "ubicacion": str(row["UBICACION"]).strip(),
                        "tipo": str(row["TIPO"]).strip(),
                        "ctd": int(row["CTD"]) if pd.notna(row["CTD"]) else 1,
                        "ml": float(row["Medidas (ml)"])
                        if pd.notna(row["Medidas (ml)"])
                        else 0.0,
                    }
                )
            if lote:
                supabase.table("productos").insert(lote).execute()
                self.matriz_message = (
                    f"Se importaron {len(lote)} productos exitosamente."
                )
                self.load_products()
        except Exception as e:
            logging.exception(f"Error handling excel upload: {e}")
            self.matriz_error = f"Error al procesar el archivo Excel: {str(e)}"

    @rx.event
    def vaciar_matriz(self):
        self.matriz_message = ""
        self.matriz_error = ""
        if not self.sel_proj_tab2:
            return
        try:
            supabase = conectar()
            if supabase:
                supabase.table("productos").delete().eq(
                    "proyecto_id", self.sel_proj_tab2
                ).execute()
                self.matriz_message = "Matriz de productos vaciada correctamente."
                self.load_products()
        except Exception as e:
            logging.exception(f"Error vaciando matriz: {e}")
            self.matriz_error = "Error al vaciar la matriz."

    @rx.event
    def select_project_tab3(self, project_id: str):
        self.sel_proj_tab3 = project_id
        self.edit_message = ""
        self.edit_error = ""
        if not project_id:
            return
        proj = next((p for p in self.projects if p["id"] == project_id), None)
        if proj:
            self.edit_nombre = proj["nombre"]
            self.edit_cliente = proj["cliente"]
            self.edit_partida = proj["partida"]
            self.edit_responsable = (
                str(proj["supervisor_id"]) if proj["supervisor_id"] else ""
            )
            self.edit_estatus = proj["estatus"]

    @rx.event
    def update_project(self):
        self.edit_message = ""
        self.edit_error = ""
        if not self.sel_proj_tab3:
            self.edit_error = "Seleccione un proyecto para editar."
            return
        try:
            supabase = conectar()
            if supabase:
                data = {
                    "proyecto_text": self.edit_nombre,
                    "cliente": self.edit_cliente,
                    "partida": self.edit_partida,
                    "supervisor_id": int(self.edit_responsable)
                    if self.edit_responsable
                    else None,
                    "estatus": self.edit_estatus,
                }
                supabase.table("proyectos").update(data).eq(
                    "id", self.sel_proj_tab3
                ).execute()
                self.edit_message = "Proyecto actualizado correctamente."
                self.load_projects()
        except Exception as e:
            logging.exception(f"Error updating project: {e}")
            self.edit_error = "Error al actualizar el proyecto."

    @rx.event
    def delete_project_full(self):
        self.edit_message = ""
        self.edit_error = ""
        if not self.sel_proj_tab3:
            return
        try:
            supabase = conectar()
            if not supabase:
                return
            res_prods = (
                supabase.table("productos")
                .select("id")
                .eq("proyecto_id", self.sel_proj_tab3)
                .execute()
            )
            if res_prods.data:
                prod_ids = [p["id"] for p in res_prods.data]
                if prod_ids:
                    supabase.table("seguimiento").delete().in_(
                        "producto_id", prod_ids
                    ).execute()
            supabase.table("incidencias").delete().eq(
                "proyecto_id", self.sel_proj_tab3
            ).execute()
            supabase.table("productos").delete().eq(
                "proyecto_id", self.sel_proj_tab3
            ).execute()
            supabase.table("proyectos").delete().eq("id", self.sel_proj_tab3).execute()
            self.edit_message = (
                "Proyecto y todos sus registros asociados eliminados correctamente."
            )
            self.sel_proj_tab3 = ""
            self.load_projects()
            if self.sel_proj_tab2 == self.sel_proj_tab3:
                self.sel_proj_tab2 = ""
                self.products_tab2 = []
        except Exception as e:
            logging.exception(f"Error deleting project completely: {e}")
            self.edit_error = "Error al eliminar el proyecto."