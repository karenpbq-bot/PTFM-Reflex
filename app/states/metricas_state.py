import reflex as rx
from app.services.base_datos import conectar, fetch_all_paginated
import logging
from typing import Any
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import io
import html as html_lib

STAGE_MAPPING = {
    "Diseño": ["Diseñado"],
    "Fabricación": ["Fabricado"],
    "Traslado": ["Material en Obra", "Material en Ubicación"],
    "Instalación": ["Instalación de Estructura", "Instalación de Puertas o Frentes"],
    "Entrega": ["Revisión y Observaciones", "Entrega"],
}
MILESTONES = [
    "Diseñado",
    "Fabricado",
    "Material en Obra",
    "Material en Ubicación",
    "Instalación de Estructura",
    "Instalación de Puertas o Frentes",
    "Revisión y Observaciones",
    "Entrega",
]


class MetricasState(rx.State):
    search_text: str = ""
    filter_responsible: str = ""
    show_planned_bars: bool = True
    selected_projects: list[str] = []
    projects_list: list[dict[str, str | int | None]] = []
    supervisores_list: list[dict[str, str | int]] = []
    gantt_html: str = '<iframe srcdoc="" style="width:100%;height:500px;border:none;" scrolling="no"></iframe>'
    stage_progress: list[dict[str, str | int | float | bool]] = []
    milestone_detail: list[dict[str, str | int | float | bool]] = []
    health_indicators: list[dict[str, str]] = []

    @rx.event
    def set_search_text(self, val: str):
        self.search_text = val
        yield MetricasState.calculate_metrics

    @rx.event
    def set_filter_responsible(self, val: str):
        self.filter_responsible = val
        yield MetricasState.calculate_metrics

    @rx.event
    def toggle_project(self, project_id: str):
        if project_id in self.selected_projects:
            self.selected_projects.remove(project_id)
        else:
            self.selected_projects.append(project_id)
        yield MetricasState.calculate_metrics

    @rx.event
    def toggle_planned_bars(self, val: bool):
        self.show_planned_bars = val
        yield MetricasState.calculate_metrics

    @rx.event
    def select_all_projects(self):
        self.selected_projects = [p["id"] for p in self.filtered_projects_list]
        yield MetricasState.calculate_metrics

    @rx.event
    def deselect_all_projects(self):
        self.selected_projects = []
        yield MetricasState.calculate_metrics

    @rx.var
    def filtered_projects_list(self) -> list[dict[str, str | int | None]]:
        projs = self.projects_list
        if self.filter_responsible:
            projs = [
                p
                for p in projs
                if str(p.get("supervisor_id", "")) == self.filter_responsible
            ]
        if self.search_text:
            projs = [
                p
                for p in projs
                if self.search_text.lower() in str(p.get("display", "")).lower()
            ]
        return projs

    @rx.event
    async def load_metricas(self):
        try:
            supabase = conectar()
            if not supabase:
                return
            res_sup = (
                supabase.table("usuarios")
                .select("id, nombre_completo")
                .in_("rol", ["admin", "Gerente", "Supervisor"])
                .execute()
            )
            if res_sup.data:
                self.supervisores_list = [
                    {"id": str(r["id"]), "nombre": r["nombre_completo"]}
                    for r in res_sup.data
                ]
            res_p = supabase.table("proyectos").select("*").execute()
            if res_p.data:
                projs = []
                for r in res_p.data:
                    projs.append(
                        {
                            "id": str(r["id"]),
                            "codigo": str(r.get("codigo", "")),
                            "nombre": str(r.get("proyecto_text", "")),
                            "cliente": str(r.get("cliente", "")),
                            "supervisor_id": str(r.get("supervisor_id", "")),
                            "display": f"[{r.get('codigo', '')}] {r.get('proyecto_text', '')}",
                            "p_dis_i": str(r.get("p_dis_i", "")),
                            "p_dis_f": str(r.get("p_dis_f", "")),
                            "p_fab_i": str(r.get("p_fab_i", "")),
                            "p_fab_f": str(r.get("p_fab_f", "")),
                            "p_tra_i": str(r.get("p_tra_i", "")),
                            "p_tra_f": str(r.get("p_tra_f", "")),
                            "p_ins_i": str(r.get("p_ins_i", "")),
                            "p_ins_f": str(r.get("p_ins_f", "")),
                            "p_ent_i": str(r.get("p_ent_i", "")),
                            "p_ent_f": str(r.get("p_ent_f", "")),
                        }
                    )
                self.projects_list = projs
                if not self.selected_projects and projs:
                    self.selected_projects = [projs[0]["id"]]
            yield MetricasState.calculate_metrics
        except Exception as e:
            logging.exception(f"Error loading metricas: {e}")

    @rx.event
    def calculate_metrics(self):
        if not self.selected_projects:
            self.gantt_html = '<div style="width:100%;min-height:500px;display:flex;align-items:center;justify-content:center;color:#9ca3af;">Seleccione proyectos para visualizar</div>'
            self.health_indicators = []
            self.stage_progress = []
            self.milestone_detail = []
            return
        try:
            supabase = conectar()
            if not supabase:
                return
            selected_p = [
                p for p in self.projects_list if p["id"] in self.selected_projects
            ]
            proj_ids = [int(p["id"]) for p in selected_p]
            res_prods = (
                supabase.table("productos")
                .select("id, proyecto_id")
                .in_("proyecto_id", proj_ids)
                .execute()
            )
            prods_df = (
                pd.DataFrame(res_prods.data)
                if res_prods.data
                else pd.DataFrame(columns=["id", "proyecto_id"])
            )
            seg_df = pd.DataFrame(columns=["producto_id", "hito", "fecha"])
            if not prods_df.empty:
                prod_ids = prods_df["id"].tolist()
                seg_data = fetch_all_paginated(
                    supabase.table("seguimiento")
                    .select("producto_id, hito, fecha")
                    .in_("producto_id", prod_ids)
                )
                if seg_data:
                    seg_df = pd.DataFrame(seg_data)
            fig = go.Figure()
            new_stage_progress = []
            new_milestone_detail = []
            new_health = []
            y_order = []
            for proj in selected_p:
                p_nom_short = proj["display"][:20]
                for stage in STAGE_MAPPING.keys():
                    if self.show_planned_bars:
                        y_order.append(f"{p_nom_short} - {stage} (Plan)")
                    y_order.append(f"{p_nom_short} - {stage} (Ejec)")
            for proj in selected_p:
                p_id = int(proj["id"])
                p_nom = proj["display"]
                p_nom_short = proj["display"][:20]
                p_prods = prods_df[prods_df["proyecto_id"] == p_id]
                total_prods = len(p_prods)
                p_segs = (
                    seg_df[seg_df["producto_id"].isin(p_prods["id"].tolist())]
                    if not p_prods.empty and (not seg_df.empty)
                    else pd.DataFrame(columns=["producto_id", "hito", "fecha"])
                )
                stage_avgs = []
                stage_prog_row = {"proyecto": p_nom}
                milestone_row = {"proyecto": p_nom}
                for m in MILESTONES:
                    c = len(p_segs[p_segs["hito"] == m]) if not p_segs.empty else 0
                    milestone_row[m] = (
                        f"{c}/{total_prods}" if total_prods > 0 else "0/0"
                    )
                new_milestone_detail.append(milestone_row)
                for stage, hitos in STAGE_MAPPING.items():
                    y_plan = f"{p_nom_short} - {stage} (Plan)"
                    y_exec = f"{p_nom_short} - {stage} (Ejec)"
                    c_total = (
                        sum((len(p_segs[p_segs["hito"] == h]) for h in hitos))
                        if not p_segs.empty
                        else 0
                    )
                    max_c = len(hitos) * total_prods
                    pct = round(c_total / max_c * 100, 1) if max_c > 0 else 0
                    stage_avgs.append(pct)
                    stage_key = (
                        stage.lower()
                        .replace("ñ", "n")
                        .replace("ó", "o")
                        .replace(" ", "_")
                    )
                    stage_prog_row[stage_key] = pct
                    stage_prog_row[f"{stage_key}_color"] = (
                        "bg-green-500"
                        if pct > 75
                        else "bg-yellow-500"
                        if pct >= 50
                        else "bg-red-500"
                    )
                    map_prefix = {
                        "Diseño": "p_dis",
                        "Fabricación": "p_fab",
                        "Traslado": "p_tra",
                        "Instalación": "p_ins",
                        "Entrega": "p_ent",
                    }[stage]
                    if self.show_planned_bars:
                        start_s = proj.get(f"{map_prefix}_i")
                        end_s = proj.get(f"{map_prefix}_f")
                        if start_s and end_s:
                            try:
                                s_dt = datetime.strptime(start_s, "%Y-%m-%d")
                                e_dt = datetime.strptime(end_s, "%Y-%m-%d")
                                if s_dt == e_dt:
                                    e_dt += timedelta(hours=23)
                                duration_ms = (e_dt - s_dt).total_seconds() * 1000
                                fig.add_trace(
                                    go.Bar(
                                        y=[y_plan],
                                        x=[duration_ms],
                                        base=[s_dt.isoformat()],
                                        orientation="h",
                                        marker_color="#87CEEB",
                                        name="Planificado",
                                        showlegend=False,
                                        opacity=0.6,
                                        hoverinfo="text",
                                        hovertext=f"Plan {stage}: {start_s} a {end_s}",
                                    )
                                )
                            except Exception:
                                logging.exception("Error building planned bars")
                    stage_segs = p_segs[p_segs["hito"].isin(hitos)]
                    if not stage_segs.empty and pct > 0:
                        try:
                            dates = pd.to_datetime(
                                stage_segs["fecha"],
                                format="%d/%m/%Y",
                                errors="coerce",
                                dayfirst=True,
                            )
                            valid_dates = dates.dropna()
                            if len(valid_dates) > 0:
                                min_date = valid_dates.min()
                                max_date = valid_dates.max()
                                if min_date == max_date:
                                    max_date += timedelta(hours=23)
                                duration_ms = (
                                    max_date - min_date
                                ).total_seconds() * 1000
                                color = (
                                    "#22c55e"
                                    if pct > 75
                                    else "#f59e0b"
                                    if pct >= 50
                                    else "#ef4444"
                                )
                                fig.add_trace(
                                    go.Bar(
                                        y=[y_exec],
                                        x=[duration_ms],
                                        base=[min_date.isoformat()],
                                        orientation="h",
                                        marker_color=color,
                                        name="Real",
                                        showlegend=False,
                                        hoverinfo="text",
                                        hovertext=f"{stage}: {pct}% ({min_date.strftime('%d/%m/%Y')} - {max_date.strftime('%d/%m/%Y')})",
                                    )
                                )
                        except Exception:
                            logging.exception("Error building actual bars")
                new_stage_progress.append(stage_prog_row)
                proj_avg = sum(stage_avgs) / len(stage_avgs) if stage_avgs else 0
                status = (
                    "Green" if proj_avg > 75 else "Yellow" if proj_avg >= 50 else "Red"
                )
                detail = (
                    "A tiempo"
                    if status == "Green"
                    else "Riesgo retraso"
                    if status == "Yellow"
                    else "Crítico"
                )
                new_health.append(
                    {
                        "project": p_nom,
                        "status": status,
                        "detail": f"{int(proj_avg)}% - {detail}",
                    }
                )
            dynamic_height = max(500, len(selected_p) * 10 * 28 + 100)
            fig.update_layout(
                barmode="group",
                height=dynamic_height,
                margin=dict(l=10, r=10, t=30, b=20),
                xaxis=dict(type="date", title=""),
                yaxis=dict(
                    title="",
                    autorange="reversed",
                    tickfont=dict(size=10),
                    categoryorder="array",
                    categoryarray=y_order,
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
                showlegend=False,
                font=dict(family="Inter, sans-serif"),
            )
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#e5e7eb")
            fig.update_yaxes(showgrid=False)
            self.stage_progress = new_stage_progress
            self.milestone_detail = new_milestone_detail
            self.health_indicators = new_health
            full_html = fig.to_html(include_plotlyjs="cdn", full_html=True)
            srcdoc_safe = full_html.replace('"', "&quot;")
            self.gantt_html = f'<iframe srcdoc="{srcdoc_safe}" style="width:100%;height:{dynamic_height}px;border:none;" scrolling="no"></iframe>'
        except Exception as e:
            logging.exception(f"Error calculating metrics: {e}")

    @rx.event
    def export_resumen_etapas(self):
        if not self.stage_progress:
            return rx.window_alert("No hay datos para exportar.")
        try:
            df = pd.DataFrame(self.stage_progress)
            output = io.StringIO()
            df.to_csv(output, index=False)
            return rx.download(data=output.getvalue(), filename="Resumen_Etapas.csv")
        except Exception as e:
            logging.exception(f"Error exporting: {e}")

    @rx.event
    def export_detalle_hitos(self):
        if not self.milestone_detail:
            return rx.window_alert("No hay datos para exportar.")
        try:
            df = pd.DataFrame(self.milestone_detail)
            output = io.StringIO()
            df.to_csv(output, index=False)
            return rx.download(data=output.getvalue(), filename="Detalle_Hitos.csv")
        except Exception as e:
            logging.exception(f"Error exporting: {e}")

    @rx.event
    async def export_auditoria(self):
        if not self.selected_projects:
            return rx.window_alert("Seleccione proyectos para auditar.")
        try:
            supabase = conectar()
            proj_ids = [int(p) for p in self.selected_projects]
            res_prods = (
                supabase.table("productos")
                .select("id, codigo_etiqueta, proyecto_id")
                .in_("proyecto_id", proj_ids)
                .execute()
            )
            if not res_prods.data:
                return rx.window_alert("No hay productos.")
            prods = res_prods.data
            p_ids = [p["id"] for p in prods]
            seg_data = fetch_all_paginated(
                supabase.table("seguimiento")
                .select("producto_id, hito")
                .in_("producto_id", p_ids)
            )
            seg_set = set(((r["producto_id"], r["hito"]) for r in seg_data))
            rows = []
            for p in prods:
                row = {"Codigo": p["codigo_etiqueta"]}
                for h in MILESTONES:
                    row[h] = 1 if (p["id"], h) in seg_set else 0
                rows.append(row)
            df = pd.DataFrame(rows)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Auditoria")
            return rx.download(data=output.getvalue(), filename="Auditoria_Piezas.xlsx")
        except Exception as e:
            logging.exception(f"Error exporting: {e}")