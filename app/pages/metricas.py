import reflex as rx
from app.components.navigation import layout
from app.states.metricas_state import MetricasState


def project_checkbox(proj: dict) -> rx.Component:
    return rx.el.label(
        rx.el.input(
            type="checkbox",
            checked=MetricasState.selected_projects.contains(proj["id"]),
            on_change=lambda _: MetricasState.toggle_project(proj["id"]),
            class_name="rounded border-gray-300 text-blue-600 focus:ring-blue-500 h-4 w-4",
        ),
        rx.el.span(proj["display"], class_name="ml-2 text-sm text-gray-700"),
        class_name="flex items-center p-2 hover:bg-gray-50 rounded-lg cursor-pointer transition-colors",
    )


def health_card(item: dict) -> rx.Component:
    status_color = rx.match(
        item["status"],
        ("Green", "bg-green-500"),
        ("Yellow", "bg-yellow-500"),
        ("Red", "bg-red-500"),
        "bg-gray-500",
    )
    return rx.el.div(
        rx.el.div(class_name=f"h-3 w-3 rounded-full {status_color} mr-3"),
        rx.el.div(
            rx.el.p(item["project"], class_name="text-sm font-bold text-gray-800"),
            rx.el.p(item["detail"], class_name="text-xs text-gray-500"),
        ),
        class_name="flex items-center p-4 bg-gray-50 rounded-xl",
    )


def stage_progress_row(item: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            item["proyecto"],
            class_name="px-4 py-3 text-sm font-semibold text-gray-900 border-b border-gray-100",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    f"{item['diseno']}%", class_name="text-xs font-bold text-gray-600"
                ),
                rx.el.div(
                    rx.el.div(
                        class_name=f"h-2 rounded-full {item['diseno_color']}",
                        style={"width": f"{item['diseno']}%"},
                    ),
                    class_name="w-full bg-gray-200 rounded-full h-2 mt-1",
                ),
            ),
            class_name="px-4 py-3 border-b border-gray-100 min-w-[120px]",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    f"{item['fabricacion']}%",
                    class_name="text-xs font-bold text-gray-600",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name=f"h-2 rounded-full {item['fabricacion_color']}",
                        style={"width": f"{item['fabricacion']}%"},
                    ),
                    class_name="w-full bg-gray-200 rounded-full h-2 mt-1",
                ),
            ),
            class_name="px-4 py-3 border-b border-gray-100 min-w-[120px]",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    f"{item['traslado']}%", class_name="text-xs font-bold text-gray-600"
                ),
                rx.el.div(
                    rx.el.div(
                        class_name=f"h-2 rounded-full {item['traslado_color']}",
                        style={"width": f"{item['traslado']}%"},
                    ),
                    class_name="w-full bg-gray-200 rounded-full h-2 mt-1",
                ),
            ),
            class_name="px-4 py-3 border-b border-gray-100 min-w-[120px]",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    f"{item['instalacion']}%",
                    class_name="text-xs font-bold text-gray-600",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name=f"h-2 rounded-full {item['instalacion_color']}",
                        style={"width": f"{item['instalacion']}%"},
                    ),
                    class_name="w-full bg-gray-200 rounded-full h-2 mt-1",
                ),
            ),
            class_name="px-4 py-3 border-b border-gray-100 min-w-[120px]",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    f"{item['entrega']}%", class_name="text-xs font-bold text-gray-600"
                ),
                rx.el.div(
                    rx.el.div(
                        class_name=f"h-2 rounded-full {item['entrega_color']}",
                        style={"width": f"{item['entrega']}%"},
                    ),
                    class_name="w-full bg-gray-200 rounded-full h-2 mt-1",
                ),
            ),
            class_name="px-4 py-3 border-b border-gray-100 min-w-[120px]",
        ),
        class_name="hover:bg-gray-50",
    )


def milestone_cell_td(item: dict, m_name: str) -> rx.Component:
    pct_key = f"{m_name}_pct"
    frac_key = f"{m_name}_frac"
    val_key = f"{m_name}_val"
    return rx.el.td(
        rx.el.div(
            rx.el.p(
                item[pct_key],
                class_name=rx.cond(
                    item[val_key].to(float) >= 75,
                    "text-sm font-bold text-green-600",
                    rx.cond(
                        item[val_key].to(float) >= 50,
                        "text-sm font-bold text-yellow-600",
                        "text-sm font-bold text-red-600",
                    ),
                ),
            ),
            rx.el.p(
                item[frac_key],
                class_name="text-[11px] text-gray-400 mt-0.5 font-medium",
            ),
            class_name="flex flex-col items-center",
        ),
        class_name="px-3 py-3 text-center border-b border-gray-100",
    )


def milestone_row(item: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            item["proyecto"],
            class_name="px-4 py-3 text-sm font-semibold text-gray-900 border-b border-gray-100",
        ),
        milestone_cell_td(item, "Diseñado"),
        milestone_cell_td(item, "Fabricado"),
        milestone_cell_td(item, "Material en Obra"),
        milestone_cell_td(item, "Material en Ubicación"),
        milestone_cell_td(item, "Instalación de Estructura"),
        milestone_cell_td(item, "Instalación de Puertas o Frentes"),
        milestone_cell_td(item, "Revisión y Observaciones"),
        milestone_cell_td(item, "Entrega"),
        class_name="hover:bg-gray-50",
    )


def collapsible_project_selector() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.icon("folder-search", class_name="h-5 w-5 text-blue-600"),
                rx.el.span(
                    "📊 Selección de Proyectos para Análisis",
                    class_name="text-lg font-bold text-gray-800",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.icon(
                rx.cond(
                    MetricasState.show_project_selector, "chevron-up", "chevron-down"
                ),
                class_name="h-5 w-5 text-gray-400",
            ),
            on_click=MetricasState.toggle_project_selector,
            class_name="flex items-center justify-between w-full p-4 hover:bg-gray-50 rounded-t-2xl transition-colors",
        ),
        rx.cond(
            MetricasState.show_project_selector,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.input(
                            placeholder="Filtrar proyectos...",
                            on_change=MetricasState.set_search_text.debounce(500),
                            class_name="w-full px-4 py-2 border border-gray-200 rounded-lg text-sm",
                        ),
                        rx.el.select(
                            rx.el.option("Todos los supervisores", value=""),
                            rx.foreach(
                                MetricasState.supervisores_list,
                                lambda s: rx.el.option(s["nombre"], value=s["id"]),
                            ),
                            on_change=MetricasState.set_filter_responsible,
                            class_name="w-full px-4 py-2 border border-gray-200 rounded-lg bg-white appearance-none text-sm",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.button(
                                "Seleccionar Todos",
                                on_click=MetricasState.select_all_projects,
                                class_name="text-sm text-blue-600 hover:text-blue-800 font-medium",
                            ),
                            rx.el.span("|", class_name="mx-2 text-gray-300"),
                            rx.el.button(
                                "Deseleccionar",
                                on_click=MetricasState.deselect_all_projects,
                                class_name="text-sm text-gray-500 hover:text-gray-700 font-medium",
                            ),
                            class_name="flex items-center",
                        ),
                        rx.el.label(
                            rx.el.input(
                                type="checkbox",
                                checked=MetricasState.show_planned_bars,
                                on_change=MetricasState.toggle_planned_bars,
                                class_name="mr-2 rounded border-gray-300 text-blue-600 focus:ring-blue-500",
                            ),
                            rx.el.span(
                                "Mostrar Planificado (Celeste)",
                                class_name="text-sm font-medium text-gray-700",
                            ),
                            class_name="flex items-center cursor-pointer",
                        ),
                        class_name="flex justify-between items-center mb-2",
                    ),
                    rx.el.div(
                        rx.foreach(
                            MetricasState.filtered_projects_list, project_checkbox
                        ),
                        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 max-h-48 overflow-y-auto border border-gray-100 p-2 rounded-xl bg-gray-50/50",
                    ),
                    class_name="px-4 pb-4",
                )
            ),
        ),
        class_name="bg-white rounded-2xl border border-gray-200 shadow-sm mb-6",
    )


def metricas_page() -> rx.Component:
    return layout(
        rx.el.div(
            collapsible_project_selector(),
            rx.radix.tabs.root(
                rx.radix.tabs.list(
                    rx.radix.tabs.trigger(
                        rx.el.span(
                            "📊 Gantt Comparativo", class_name="flex items-center gap-2"
                        ),
                        value="gantt",
                        class_name="px-4 py-2 font-semibold text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 outline-none",
                    ),
                    rx.radix.tabs.trigger(
                        rx.el.span(
                            "📋 Tablas y Exportación",
                            class_name="flex items-center gap-2",
                        ),
                        value="tablas",
                        class_name="px-4 py-2 font-semibold text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 outline-none",
                    ),
                    class_name="flex gap-4 border-b border-gray-200 mb-6",
                ),
                rx.radix.tabs.content(
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h3("Gantt", class_name="text-lg font-bold"),
                                    rx.el.div(
                                        rx.el.div(
                                            rx.el.div(
                                                class_name="w-3 h-3 rounded-full bg-[#87CEEB] mr-1"
                                            ),
                                            rx.el.span(
                                                "Planificado",
                                                class_name="text-xs text-gray-500",
                                            ),
                                            class_name="flex items-center mr-3",
                                        ),
                                        rx.el.div(
                                            rx.el.div(
                                                class_name="w-3 h-3 rounded-full bg-[#22c55e] mr-1"
                                            ),
                                            rx.el.span(
                                                ">75%",
                                                class_name="text-xs text-gray-500",
                                            ),
                                            class_name="flex items-center mr-3",
                                        ),
                                        rx.el.div(
                                            rx.el.div(
                                                class_name="w-3 h-3 rounded-full bg-[#f59e0b] mr-1"
                                            ),
                                            rx.el.span(
                                                "50-75%",
                                                class_name="text-xs text-gray-500",
                                            ),
                                            class_name="flex items-center mr-3",
                                        ),
                                        rx.el.div(
                                            rx.el.div(
                                                class_name="w-3 h-3 rounded-full bg-[#ef4444] mr-1"
                                            ),
                                            rx.el.span(
                                                "<50%",
                                                class_name="text-xs text-gray-500",
                                            ),
                                            class_name="flex items-center",
                                        ),
                                        class_name="flex items-center",
                                    ),
                                    class_name="flex justify-between items-center mb-6",
                                ),
                                rx.html(MetricasState.gantt_html),
                                class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm lg:col-span-3 min-h-[500px] overflow-auto",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    "Salud de Gestión",
                                    class_name="text-lg font-bold mb-6",
                                ),
                                rx.el.div(
                                    rx.foreach(
                                        MetricasState.health_indicators, health_card
                                    ),
                                    class_name="flex flex-col gap-3 max-h-[500px] overflow-y-auto pr-2",
                                ),
                                class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm lg:col-span-1",
                            ),
                            class_name="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8",
                        )
                    ),
                    value="gantt",
                    class_name="outline-none",
                ),
                rx.radix.tabs.content(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Avances por Etapa", class_name="text-lg font-bold mb-4"
                            ),
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(
                                                "Proyecto",
                                                class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Diseño",
                                                class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Fabricación",
                                                class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Traslado",
                                                class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Instalación",
                                                class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Entrega",
                                                class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                        )
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(
                                            MetricasState.stage_progress,
                                            stage_progress_row,
                                        )
                                    ),
                                    class_name="min-w-full table-auto border-separate border-spacing-0",
                                ),
                                class_name="overflow-x-auto rounded-xl border border-gray-200",
                            ),
                            class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm mb-6",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Detalle por Hito Individual",
                                class_name="text-lg font-bold mb-4",
                            ),
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(
                                                "Proyecto",
                                                class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Diseñado",
                                                class_name="px-4 py-2 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Fabricado",
                                                class_name="px-4 py-2 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Material en Obra",
                                                class_name="px-4 py-2 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Material en Ubicación",
                                                class_name="px-4 py-2 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Inst. Estructura",
                                                class_name="px-4 py-2 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Inst. Puertas",
                                                class_name="px-4 py-2 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Revisión",
                                                class_name="px-4 py-2 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                            rx.el.th(
                                                "Entrega",
                                                class_name="px-4 py-2 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200",
                                            ),
                                        )
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(
                                            MetricasState.milestone_detail,
                                            milestone_row,
                                        )
                                    ),
                                    class_name="min-w-full table-auto border-separate border-spacing-0",
                                ),
                                class_name="overflow-x-auto rounded-xl border border-gray-200",
                            ),
                            class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm mb-6",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Exportación de Resultados",
                                class_name="text-lg font-bold mb-4",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    rx.icon("download", class_name="w-4 h-4 mr-2"),
                                    "Resumen Etapas (CSV)",
                                    on_click=MetricasState.export_resumen_etapas,
                                    class_name="flex items-center justify-center px-4 py-3 bg-blue-50 hover:bg-blue-100 text-blue-700 font-bold rounded-xl transition-colors",
                                ),
                                rx.el.button(
                                    rx.icon("download", class_name="w-4 h-4 mr-2"),
                                    "Detalle Hitos (CSV)",
                                    on_click=MetricasState.export_detalle_hitos,
                                    class_name="flex items-center justify-center px-4 py-3 bg-purple-50 hover:bg-purple-100 text-purple-700 font-bold rounded-xl transition-colors",
                                ),
                                rx.el.button(
                                    rx.icon(
                                        "file-spreadsheet", class_name="w-4 h-4 mr-2"
                                    ),
                                    "Auditoría Piezas (0/1)",
                                    on_click=MetricasState.export_auditoria,
                                    class_name="flex items-center justify-center px-4 py-3 bg-green-50 hover:bg-green-100 text-green-700 font-bold rounded-xl transition-colors",
                                ),
                                class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
                            ),
                            class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm",
                        ),
                    ),
                    value="tablas",
                    class_name="outline-none",
                ),
                default_value="gantt",
            ),
            class_name="max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700",
        ),
        "Métricas",
    )