import reflex as rx
from typing import TypedDict, Any
from app.services.base_datos import (
    conectar,
    sincronizar_avances_estructural,
    fetch_all_paginated,
)
from app.states.login_state import LoginState
from datetime import datetime
import pandas as pd
import logging
import os


class SeguimientoProject(TypedDict):
    id: str
    label: str
    codigo: str


class SeguimientoProduct(TypedDict):
    id: int
    codigo_etiqueta: str
    ubicacion: str
    tipo: str
    ml: float
    ctd: int


class SeguimientoState(rx.State):
    search_text: str = ""
    selected_project_id: str = ""
    selected_project_label: str = ""
    selected_project_codigo: str = ""
    projects_list: list[SeguimientoProject] = []
    group_by: str = "none"
    primary_filter: str = ""
    refinement_filter: str = ""
    all_products: list[SeguimientoProduct] = []
    db_checks: list[str] = []
    pending_checks: list[str] = []
    delete_pending: list[str] = []
    product_notes: dict[str, str] = {}
    current_user_role: str = ""
    show_project_selector: bool = True
    show_advanced_config: bool = False
    milestone_names: list[str] = [
        "Diseñado",
        "Fabricado",
        "Material en Obra",
        "Material en Ubicación",
        "Instalación de Estructura",
        "Instalación de Puertas o Frentes",
        "Revisión y Observaciones",
        "Entrega",
    ]
    milestone_weights: dict[str, float] = {
        "Diseñado": 15,
        "Fabricado": 40,
        "Material en Obra": 5,
        "Material en Ubicación": 5,
        "Instalación de Estructura": 15,
        "Instalación de Puertas o Frentes": 10,
        "Revisión y Observaciones": 5,
        "Entrega": 5,
    }

    @rx.var
    def is_jefe(self) -> bool:
        return self.current_user_role.lower() in ["admin", "administrador", "gerente"]

    @rx.event
    def is_supervisor_only(self) -> bool:
        return ~SeguimientoState.is_jefe

    @rx.event
    def set_search_text(self, val: str):
        self.search_text = val
        yield SeguimientoState.load_projects_list

    @rx.event
    def set_primary_filter(self, val: str):
        self.primary_filter = val

    @rx.event
    def set_refinement_filter(self, val: str):
        self.refinement_filter = val

    @rx.event
    def set_group_by(self, val: str):
        self.group_by = val

    @rx.event
    def toggle_project_selector(self):
        self.show_project_selector = not self.show_project_selector

    @rx.event
    def toggle_advanced_config(self):
        self.show_advanced_config = not self.show_advanced_config

    @rx.event
    def set_product_note(self, product_id: str, value: str):
        self.product_notes[product_id] = value

    @rx.event
    def set_milestone_weight(self, hito: str, value: str):
        try:
            self.milestone_weights[hito] = float(value)
        except:
            logging.exception("Unexpected error")

    @rx.event
    async def load_projects_list(self):
        try:
            login_state = await self.get_state(LoginState)
            self.current_user_role = login_state.user_role
            supabase = conectar()
            if not supabase:
                return
            query = supabase.table("proyectos").select(
                "id, codigo, proyecto_text, cliente"
            )
            if self.search_text:
                query = query.or_(
                    f"codigo.ilike.%{self.search_text}%,proyecto_text.ilike.%{self.search_text}%,cliente.ilike.%{self.search_text}%"
                )
            res = query.order("created_at", desc=True).execute()
            if res.data:
                self.projects_list = [
                    {
                        "id": str(r["id"]),
                        "label": f"[{r['codigo']}] {r['proyecto_text']}",
                        "codigo": str(r["codigo"]),
                    }
                    for r in res.data
                ]
            else:
                self.projects_list = []
        except Exception as e:
            logging.exception(f"Error loading projects: {e}")
            self.projects_list = []

    @rx.event
    def select_project(self, project_id: str):
        self.selected_project_id = project_id
        proj = next((p for p in self.projects_list if p["id"] == project_id), None)
        if proj:
            self.selected_project_label = proj["label"]
            self.selected_project_codigo = proj["codigo"]
        else:
            self.selected_project_label = ""
            self.selected_project_codigo = ""
        yield SeguimientoState.load_products_and_seguimiento

    @rx.event
    async def load_products_and_seguimiento(self):
        if not self.selected_project_id:
            self.all_products = []
            self.db_checks = []
            self.pending_checks = []
            self.delete_pending = []
            self.product_notes = {}
            return
        try:
            login_state = await self.get_state(LoginState)
            self.current_user_role = login_state.user_role
            supabase = conectar()
            if not supabase:
                return
            res_prods = (
                supabase.table("productos")
                .select("id, codigo_etiqueta, ubicacion, tipo, ml, ctd")
                .eq("proyecto_id", self.selected_project_id)
                .execute()
            )
            if not res_prods.data:
                self.all_products = []
                self.db_checks = []
                self.pending_checks = []
                self.product_notes = {}
                return
            self.all_products = [
                {
                    "id": int(r["id"]),
                    "codigo_etiqueta": str(r.get("codigo_etiqueta", "")),
                    "ubicacion": str(r.get("ubicacion", "")),
                    "tipo": str(r.get("tipo", "")),
                    "ml": float(r.get("ml", 0)),
                    "ctd": int(r.get("ctd", 0)),
                }
                for r in res_prods.data
            ]
            prod_ids = [p["id"] for p in self.all_products]
            seg_data = fetch_all_paginated(
                supabase.table("seguimiento")
                .select("producto_id, hito")
                .in_("producto_id", prod_ids)
            )
            if seg_data:
                self.db_checks = [f"{r['producto_id']}_{r['hito']}" for r in seg_data]
            else:
                self.db_checks = []
            notes_data = fetch_all_paginated(
                supabase.table("seguimiento")
                .select("producto_id, observaciones")
                .in_("producto_id", prod_ids)
                .not_.is_("observaciones", "null")
            )
            notes_map = {}
            for r in notes_data:
                pid = str(r["producto_id"])
                obs = r.get("observaciones", "")
                if obs and obs.strip() and (pid not in notes_map):
                    notes_map[pid] = obs.strip()
            self.product_notes = notes_map
            self.pending_checks = []
        except Exception as e:
            logging.exception(f"Error loading products/seguimiento: {e}")

    @rx.var
    def filtered_products(self) -> list[SeguimientoProduct]:
        prods = self.all_products
        if self.primary_filter:
            prods = [
                p
                for p in prods
                if self.primary_filter.lower() in p["codigo_etiqueta"].lower()
                or self.primary_filter.lower() in p["ubicacion"].lower()
                or self.primary_filter.lower() in p["tipo"].lower()
            ]
        if self.refinement_filter:
            prods = [
                p
                for p in prods
                if self.refinement_filter.lower() in p["codigo_etiqueta"].lower()
                or self.refinement_filter.lower() in p["ubicacion"].lower()
                or self.refinement_filter.lower() in p["tipo"].lower()
            ]
        if self.group_by == "sin_avance":
            filtered = []
            for p in prods:
                has_any = False
                for m in self.milestone_names:
                    k = f"{p['id']}_{m}"
                    if k in self.db_checks or k in self.pending_checks:
                        has_any = True
                        break
                if not has_any:
                    filtered.append(p)
            prods = filtered
        elif self.group_by == "ubicacion":
            prods = sorted(prods, key=lambda x: x["ubicacion"])
        elif self.group_by == "tipo":
            prods = sorted(prods, key=lambda x: x["tipo"])
        elif self.group_by.startswith("sin_hito_"):
            try:
                hito_idx = int(self.group_by.split("_")[-1])
                if 0 <= hito_idx < len(self.milestone_names):
                    target_hito = self.milestone_names[hito_idx]
                    filtered = []
                    for p in prods:
                        k = f"{p['id']}_{target_hito}"
                        if k not in self.db_checks and k not in self.pending_checks:
                            filtered.append(p)
                    prods = filtered
            except (ValueError, IndexError):
                logging.exception("Unexpected error")
        return prods

    @rx.event
    async def bulk_mark_hito(self, hito_idx: int):
        """Mark all currently filtered products for the given milestone (and all previous ones)."""
        login_state = await self.get_state(LoginState)
        self.current_user_role = login_state.user_role
        prods = self.filtered_products
        for p in prods:
            product_id = str(p["id"])
            for i in range(int(hito_idx) + 1):
                h_name = self.milestone_names[i]
                c_key = f"{product_id}_{h_name}"
                if c_key not in self.db_checks and c_key not in self.pending_checks:
                    self.pending_checks.append(c_key)

    @rx.event
    async def toggle_check(self, product_id: str, hito_idx: int):
        login_state = await self.get_state(LoginState)
        self.current_user_role = login_state.user_role
        hito_name = self.milestone_names[int(hito_idx)]
        check_key = f"{product_id}_{hito_name}"
        is_jefe = self.current_user_role.lower() in [
            "admin",
            "administrador",
            "gerente",
        ]
        if check_key in self.db_checks:
            if is_jefe:
                if check_key in self.delete_pending:
                    self.delete_pending.remove(check_key)
                else:
                    self.delete_pending.append(check_key)
            return
        if check_key in self.pending_checks:
            if is_jefe:
                for i in range(int(hito_idx), len(self.milestone_names)):
                    h_name = self.milestone_names[i]
                    c_key = f"{product_id}_{h_name}"
                    if c_key in self.pending_checks:
                        self.pending_checks.remove(c_key)
            return
        for i in range(int(hito_idx) + 1):
            h_name = self.milestone_names[i]
            c_key = f"{product_id}_{h_name}"
            if c_key not in self.db_checks and c_key not in self.pending_checks:
                self.pending_checks.append(c_key)

    @rx.event
    async def borrar_avance(self):
        if not self.delete_pending:
            return
        login_state = await self.get_state(LoginState)
        self.current_user_role = login_state.user_role
        is_jefe = self.current_user_role.lower() in [
            "admin",
            "administrador",
            "gerente",
        ]
        if not is_jefe:
            return
        try:
            supabase = conectar()
            if not supabase:
                return
            for c_key in self.delete_pending:
                parts = c_key.split("_", 1)
                pid = int(parts[0])
                hito = parts[1]
                supabase.table("seguimiento").delete().eq("producto_id", pid).eq(
                    "hito", hito
                ).execute()
                if c_key in self.db_checks:
                    self.db_checks.remove(c_key)
            self.delete_pending = []
            if self.selected_project_codigo:
                sincronizar_avances_estructural(self.selected_project_codigo)
        except Exception as e:
            logging.exception(f"Error deleting avances: {e}")
            return rx.window_alert(f"Error al borrar avance: {str(e)}")

    @rx.event
    async def guardar_avance(self):
        if not self.pending_checks:
            return
        try:
            login_state = await self.get_state(LoginState)
            supabase = conectar()
            if not supabase:
                return
            lote = []
            fecha_str = datetime.now().strftime("%d/%m/%Y")
            for c in self.pending_checks:
                parts = c.split("_", 1)
                lote.append(
                    {"producto_id": int(parts[0]), "hito": parts[1], "fecha": fecha_str}
                )
                self.db_checks.append(c)
            if lote:
                supabase.table("seguimiento").upsert(
                    lote, on_conflict="producto_id, hito"
                ).execute()
            for pid_str, note_text in self.product_notes.items():
                if note_text.strip():
                    pid_int = int(pid_str)
                    supabase.table("seguimiento").update(
                        {"observaciones": note_text}
                    ).eq("producto_id", pid_int).execute()
            if self.selected_project_codigo:
                sincronizar_avances_estructural(self.selected_project_codigo)
            self.pending_checks = []
        except Exception as e:
            logging.exception(f"Error saving avances: {e}")

    @rx.event
    def limpiar_marcacion(self):
        self.pending_checks = []
        self.delete_pending = []

    @rx.event
    def borrar_avances(self, product_id: str, hito_idx: int):
        try:
            supabase = conectar()
            if not supabase:
                return
            keys_to_delete = []
            hitos_to_delete = []
            for i in range(int(hito_idx), len(self.milestone_names)):
                h_name = self.milestone_names[i]
                c_key = f"{product_id}_{h_name}"
                if c_key in self.db_checks:
                    keys_to_delete.append(c_key)
                    hitos_to_delete.append(h_name)
            if hitos_to_delete:
                supabase.table("seguimiento").delete().eq(
                    "producto_id", int(product_id)
                ).in_("hito", hitos_to_delete).execute()
                for k in keys_to_delete:
                    self.db_checks.remove(k)
        except Exception as e:
            logging.exception(f"Error deleting avance: {e}")

    @rx.var
    def avance_total(self) -> float:
        if not self.all_products:
            return 0.0
        total_weight = 0.0
        for p in self.all_products:
            for m in self.milestone_names:
                k = f"{p['id']}_{m}"
                if k in self.db_checks or k in self.pending_checks:
                    total_weight += self.milestone_weights.get(m, 0)
        return round(total_weight / len(self.all_products), 2)

    @rx.var
    def avance_seleccion(self) -> float:
        prods = self.filtered_products
        if not prods:
            return 0.0
        total_weight = 0.0
        for p in prods:
            for m in self.milestone_names:
                k = f"{p['id']}_{m}"
                if k in self.db_checks or k in self.pending_checks:
                    total_weight += self.milestone_weights.get(m, 0)
        return round(total_weight / len(prods), 2)

    @rx.event
    def export_seguimiento(self):
        if not self.selected_project_id or not self.all_products:
            return rx.window_alert("No hay datos para exportar.")
        try:
            import pandas as pd
            import io

            supabase = conectar()
            if not supabase:
                return rx.window_alert("Error de conexión.")
            prod_ids = [p["id"] for p in self.all_products]
            seg_data = fetch_all_paginated(
                supabase.table("seguimiento")
                .select("producto_id, hito, fecha")
                .in_("producto_id", prod_ids)
            )
            seg_lookup = {}
            for r in seg_data:
                seg_lookup[r["producto_id"], r["hito"]] = r.get("fecha", "")
            hitos = [
                "Diseñado",
                "Fabricado",
                "Material en Obra",
                "Material en Ubicación",
                "Instalación de Estructura",
                "Instalación de Puertas o Frentes",
                "Revisión y Observaciones",
                "Entrega",
            ]
            rows = []
            for p in self.all_products:
                row = {
                    "Código": p["codigo_etiqueta"],
                    "Ubicación": p["ubicacion"],
                    "Tipo": p["tipo"],
                    "ML": p["ml"],
                    "Ctd": p["ctd"],
                }
                for h in hitos:
                    row[h] = seg_lookup.get((p["id"], h), "")
                rows.append(row)
            df = pd.DataFrame(rows)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Avance")
            filename = f"Avance_{self.selected_project_codigo or 'proyecto'}.xlsx"
            return rx.download(data=output.getvalue(), filename=filename)
        except Exception as e:
            logging.exception(f"Error exporting: {e}")
            return rx.window_alert(f"Error al exportar: {str(e)}")

    @rx.event
    async def handle_import_seguimiento(self, files: list[rx.UploadFile]):
        """Import seguimiento from Excel. Only updates empty cells, preserves existing data."""
        if not self.selected_project_id or not self.all_products:
            yield rx.window_alert("Seleccione un proyecto con productos primero.")
            return
        if not files:
            return
        try:
            import pandas as pd
            import io

            file = files[0]
            upload_data = await file.read()
            df = pd.read_excel(io.BytesIO(upload_data))
            code_col = None
            for col_name in ["Código", "Código ID", "codigo_etiqueta"]:
                if col_name in df.columns:
                    code_col = col_name
                    break
            if code_col is None:
                yield rx.window_alert(
                    "El archivo no tiene columna de código (Código, Código ID)."
                )
                return
            hitos = [
                "Diseñado",
                "Fabricado",
                "Material en Obra",
                "Material en Ubicación",
                "Instalación de Estructura",
                "Instalación de Puertas o Frentes",
                "Revisión y Observaciones",
                "Entrega",
            ]
            found_hitos = [h for h in hitos if h in df.columns]
            if not found_hitos:
                yield rx.window_alert(
                    "El archivo no contiene columnas de hitos válidas."
                )
                return
            code_to_id = {p["codigo_etiqueta"]: p["id"] for p in self.all_products}
            supabase = conectar()
            if not supabase:
                yield rx.window_alert("Error de conexión a la base de datos.")
                return
            prod_ids = [p["id"] for p in self.all_products]
            existing_data = fetch_all_paginated(
                supabase.table("seguimiento")
                .select("producto_id, hito")
                .in_("producto_id", prod_ids)
            )
            existing_set = set()
            for r in existing_data:
                existing_set.add((r["producto_id"], r["hito"]))
            lote = []
            skipped = 0
            for _, row in df.iterrows():
                codigo = str(row[code_col]).strip()
                pid = code_to_id.get(codigo)
                if pid is None:
                    continue
                for h in found_hitos:
                    cell_value = row.get(h)
                    if pd.notna(cell_value) and str(cell_value).strip() != "":
                        if (pid, h) not in existing_set:
                            fecha_str = str(cell_value).strip()
                            if hasattr(cell_value, "strftime"):
                                fecha_str = cell_value.strftime("%d/%m/%Y")
                            lote.append(
                                {"producto_id": pid, "hito": h, "fecha": fecha_str}
                            )
                        else:
                            skipped += 1
            if lote:
                for i in range(0, len(lote), 500):
                    batch = lote[i : i + 500]
                    supabase.table("seguimiento").upsert(
                        batch, on_conflict="producto_id, hito"
                    ).execute()
                if self.selected_project_codigo:
                    sincronizar_avances_estructural(self.selected_project_codigo)
                yield SeguimientoState.load_products_and_seguimiento
                yield rx.window_alert(
                    f"Importación completada: {len(lote)} registros nuevos agregados. {skipped} ya existían y se conservaron."
                )
                return
            else:
                yield rx.window_alert(
                    f"No se encontraron registros nuevos para importar. {skipped} ya existían en la base de datos."
                )
                return
        except Exception as e:
            logging.exception(f"Error importing seguimiento: {e}")
            yield rx.window_alert(f"Error al importar: {str(e)}")
            return