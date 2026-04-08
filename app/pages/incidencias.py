import reflex as rx
from app.components.navigation import layout
from app.states.incidencias_state import (
    IncidenciasState,
    IncidenciaData,
    TechnicalRequirement,
    PieceData,
)


def summary_card(label: str, value: int, color_class: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-sm text-gray-500 font-bold uppercase"),
        rx.el.p(
            value.to_string(), class_name=f"text-3xl font-black {color_class} mt-1"
        ),
        class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm flex-1",
    )


def incidencia_card(inc: IncidenciaData) -> rx.Component:
    priority_styles = rx.match(
        inc["priority"],
        ("Alta", "bg-red-100 text-red-600"),
        ("Media", "bg-yellow-100 text-yellow-600"),
        ("Baja", "bg-green-100 text-green-600"),
        "bg-gray-100 text-gray-600",
    )
    status_styles = rx.match(
        inc["status"],
        ("Abierta", "bg-red-500 text-white"),
        ("En Proceso", "bg-blue-500 text-white"),
        ("Resuelta", "bg-green-500 text-white"),
        "bg-gray-500 text-white",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(inc["id"], class_name="text-xs font-bold text-gray-400"),
                rx.el.h4(inc["project"], class_name="text-lg font-bold text-gray-900"),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.span(
                    inc["priority"],
                    class_name=f"px-2 py-1 rounded-lg text-[10px] font-bold uppercase {priority_styles}",
                ),
                rx.el.span(
                    inc["status"],
                    class_name=f"px-2 py-1 rounded-lg text-[10px] font-bold uppercase {status_styles}",
                ),
                class_name="flex gap-2",
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.p(
            inc["description"], class_name="text-sm text-gray-600 mb-6 font-medium"
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("user", class_name="h-4 w-4 text-gray-400"),
                rx.el.span(
                    inc["assigned"], class_name="text-xs font-bold text-gray-700"
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.icon("calendar", class_name="h-4 w-4 text-gray-400"),
                rx.el.span(inc["date"], class_name="text-xs font-bold text-gray-700"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex justify-between pt-4 border-t border-gray-100",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm",
    )


def piece_row(piece: PieceData) -> rx.Component:
    prio_color = rx.match(
        piece["priority"],
        ("Alta", "text-red-500"),
        ("Media", "text-yellow-500"),
        ("Baja", "text-green-500"),
        "text-gray-500",
    )
    return rx.el.tr(
        rx.el.td(piece["id"], class_name="px-4 py-3 text-xs font-bold text-gray-500"),
        rx.el.td(
            piece["name"], class_name="px-4 py-3 text-sm font-semibold text-gray-900"
        ),
        rx.el.td(piece["status"], class_name="px-4 py-3 text-sm text-gray-600"),
        rx.el.td(piece["responsible"], class_name="px-4 py-3 text-sm text-gray-600"),
        rx.el.td(
            piece["priority"], class_name=f"px-4 py-3 text-sm font-bold {prio_color}"
        ),
        class_name="hover:bg-gray-50 border-b border-gray-100",
    )


def requirement_item(req: TechnicalRequirement) -> rx.Component:
    status_bg = rx.match(
        req["status"],
        ("Cumplido", "bg-green-100 text-green-600"),
        ("En Verificación", "bg-blue-100 text-blue-600"),
        ("Pendiente", "bg-red-100 text-red-600"),
        "bg-gray-100 text-gray-600",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                req["project"],
                class_name="text-[10px] font-bold text-gray-400 uppercase",
            ),
            rx.el.p(
                req["requirement"], class_name="text-sm font-semibold text-gray-800"
            ),
        ),
        rx.el.span(
            req["status"],
            class_name=f"px-2 py-1 rounded-md text-[10px] font-bold uppercase {status_bg}",
        ),
        class_name="flex justify-between items-center p-4 bg-gray-50 rounded-xl",
    )


def incidencias_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                summary_card(
                    "Total", IncidenciasState.total_incidencias, "text-gray-900"
                ),
                summary_card(
                    "Abiertas", IncidenciasState.abiertas_count, "text-red-500"
                ),
                summary_card(
                    "En Proceso", IncidenciasState.proceso_count, "text-blue-500"
                ),
                summary_card(
                    "Resueltas", IncidenciasState.resueltas_count, "text-green-500"
                ),
                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Listado de Incidencias",
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        rx.el.div(
                            rx.el.input(
                                placeholder="Buscar incidencia...",
                                class_name="px-4 py-2 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-full sm:w-64",
                            ),
                            rx.icon(
                                "search",
                                class_name="absolute right-3 top-2.5 h-4 w-4 text-gray-400",
                            ),
                            class_name="relative",
                        ),
                        class_name="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(IncidenciasState.incidencias, incidencia_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Requerimientos Técnicos",
                            class_name="text-lg font-bold text-gray-900 mb-6",
                        ),
                        rx.el.div(
                            rx.foreach(
                                IncidenciasState.tech_requirements, requirement_item
                            ),
                            class_name="flex flex-col gap-4",
                        ),
                        class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Gestión de Piezas",
                            class_name="text-lg font-bold text-gray-900 mb-6",
                        ),
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "ID",
                                            class_name="px-4 py-2 text-left text-[10px] font-bold text-gray-400 uppercase",
                                        ),
                                        rx.el.th(
                                            "Pieza",
                                            class_name="px-4 py-2 text-left text-[10px] font-bold text-gray-400 uppercase",
                                        ),
                                        rx.el.th(
                                            "Estado",
                                            class_name="px-4 py-2 text-left text-[10px] font-bold text-gray-400 uppercase",
                                        ),
                                        rx.el.th(
                                            "Resp.",
                                            class_name="px-4 py-2 text-left text-[10px] font-bold text-gray-400 uppercase",
                                        ),
                                        rx.el.th(
                                            "Prio.",
                                            class_name="px-4 py-2 text-left text-[10px] font-bold text-gray-400 uppercase",
                                        ),
                                    ),
                                    class_name="bg-gray-50",
                                ),
                                rx.el.tbody(
                                    rx.foreach(IncidenciasState.pieces, piece_row)
                                ),
                                class_name="w-full table-auto",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm lg:col-span-2",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
                ),
                class_name="animate-in fade-in slide-in-from-bottom-4 duration-700",
            ),
            class_name="max-w-7xl mx-auto",
        ),
        "Incidencias y Requerimientos",
    )