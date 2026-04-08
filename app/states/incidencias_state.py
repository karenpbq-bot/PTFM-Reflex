import reflex as rx
from typing import TypedDict
from app.services.base_datos import obtener_incidencias_resumen
import logging


class IncidenciaData(TypedDict):
    id: str
    project: str
    description: str
    priority: str
    status: str
    date: str
    assigned: str


class TechnicalRequirement(TypedDict):
    project: str
    requirement: str
    status: str


class PieceData(TypedDict):
    id: str
    name: str
    status: str
    responsible: str
    priority: str


class IncidenciasState(rx.State):
    incidencias: list[IncidenciaData] = []
    tech_requirements: list[TechnicalRequirement] = [
        {
            "project": "Banda X1",
            "requirement": "Certificación IP65 en motores",
            "status": "Cumplido",
        },
        {
            "project": "Banda X1",
            "requirement": "Velocidad variable 0-2m/s",
            "status": "En Verificación",
        },
        {
            "project": "Z-Core",
            "requirement": "Precisión +-0.01mm",
            "status": "Pendiente",
        },
    ]
    pieces: list[PieceData] = [
        {
            "id": "PC-101",
            "name": "Rodamiento SKF",
            "status": "En Stock",
            "responsible": "Almacen Central",
            "priority": "Alta",
        },
        {
            "id": "PC-102",
            "name": "Piston SMC",
            "status": "Pedido",
            "responsible": "Compras",
            "priority": "Media",
        },
        {
            "id": "PC-103",
            "name": "PLC Siemens S7",
            "status": "En Stock",
            "responsible": "Electronica",
            "priority": "Baja",
        },
    ]

    @rx.event
    def load_incidencias(self):
        try:
            df_inc = obtener_incidencias_resumen()
            if df_inc.empty:
                self.incidencias = []
                return
            loaded: list[IncidenciaData] = []
            for _, row in df_inc.iterrows():
                cat = str(row.get("categoria", ""))
                priority = (
                    "Alta"
                    if cat in ["Faltante", "Pieza Dañada"]
                    else "Media"
                    if cat == "Cambio"
                    else "Baja"
                )
                raw_date = str(row.get("created_at", ""))
                date_str = raw_date[:10] if raw_date else ""
                loaded.append(
                    {
                        "id": f"REQ-{row.get('id', '')}",
                        "project": str(row.get("proyecto_text", "Sin Proyecto")),
                        "description": str(row.get("tipo_requerimiento", "")),
                        "priority": priority,
                        "status": str(row.get("estado", "Pendiente")),
                        "date": date_str,
                        "assigned": "Supervisor",
                    }
                )
            self.incidencias = loaded
        except Exception as e:
            logging.exception(f"Error loading incidencias: {e}")
            self.incidencias = []

    @rx.var
    def total_incidencias(self) -> int:
        return len(self.incidencias)

    @rx.var
    def abiertas_count(self) -> int:
        return len(
            [i for i in self.incidencias if i["status"] in ["Pendiente", "Abierta"]]
        )

    @rx.var
    def proceso_count(self) -> int:
        return len([i for i in self.incidencias if i["status"] == "En Proceso"])

    @rx.var
    def resueltas_count(self) -> int:
        return len([i for i in self.incidencias if i["status"] == "Resuelta"])