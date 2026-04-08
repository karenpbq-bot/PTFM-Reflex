import reflex as rx
from app.components.navigation import layout
from app.states.metricas_state import MetricasState


def kpi_card(label: str, value: str, trend: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-sm text-gray-500 font-medium"),
            rx.el.p(value, class_name="text-3xl font-bold text-gray-900 mt-1"),
            rx.el.p(trend, class_name="text-xs text-green-500 font-bold mt-2"),
            class_name="flex-1",
        ),
        rx.icon(icon, class_name="h-8 w-8 text-blue-100"),
        class_name="flex items-start p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
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


def milestone_row(item: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            item["proyecto"],
            class_name="px-4 py-3 text-sm font-semibold text-gray-900 border-b border-gray-100",
        ),
        rx.el.td(
            f"{item['Diseñado']}%",
            class_name="px-4 py-3 text-sm text-gray-600 text-center border-b border-gray-100",
        ),
        rx.el.td(
            f"{item['Fabricado']}%",
            class_name="px-4 py-3 text-sm text-gray-600 text-center border-b border-gray-100",
        ),
        rx.el.td(
            f"{item['Material en Obra']}%",
            class_name="px-4 py-3 text-sm text-gray-600 text-center border-b border-gray-100",
        ),
        rx.el.td(
            f"{item['Material en Ubicación']}%",
            class_name="px-4 py-3 text-sm text-gray-600 text-center border-b border-gray-100",
        ),
        rx.el.td(
            f"{item['Instalación de Estructura']}%",
            class_name="px-4 py-3 text-sm text-gray-600 text-center border-b border-gray-100",
        ),
        rx.el.td(
            f"{item['Instalación de Puertas o Frentes']}%",
            class_name="px-4 py-3 text-sm text-gray-600 text-center border-b border-gray-100",
        ),
        rx.el.td(
            f"{item['Revisión y Observaciones']}%",
            class_name="px-4 py-3 text-sm text-gray-600 text-center border-b border-gray-100",
        ),
        rx.el.td(
            f"{item['Entrega']}%",
            class_name="px-4 py-3 text-sm text-gray-600 text-center border-b border-gray-100",
        ),
        class_name="hover:bg-gray-50",
    )


def metricas_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Selección de Proyectos para Análisis",
                    class_name="text-lg font-bold text-gray-800 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.input(
                            placeholder="Filtrar por código o nombre...",
                            on_change=MetricasState.set_search_text.debounce(500),
                            class_name="w-full px-4 py-2 border border-gray-200 rounded-lg",
                        ),
                        rx.el.button(
                            "Aplicar Filtro",
                            on_click=MetricasState.load_metricas,
                            class_name="px-4 py-2 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition-colors",
                        ),
                        class_name="flex gap-3 mb-4",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.foreach(
                                MetricasState.projects_list,
                                lambda p: rx.el.option(p["display"], value=p["id"]),
                            ),
                            on_change=MetricasState.set_selected_projects,
                            class_name="w-full px-4 py-2 border border-gray-200 rounded-lg bg-white appearance-none",
                        ),
                        class_name="w-full",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm mb-6",
            ),
            rx.el.div(
                kpi_card(
                    "Presupuesto (Uso Estimado)",
                    MetricasState.budget_utilization,
                    "+2.5% vs mes ant",
                    "banknote",
                ),
                kpi_card(
                    "Cronograma (Adherencia)",
                    MetricasState.timeline_adherence,
                    "+1.2% estable",
                    "calendar-check",
                ),
                kpi_card(
                    "Recursos (Asignación)",
                    MetricasState.resource_allocation,
                    "Óptimo",
                    "users",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Cronograma de Proyectos", class_name="text-lg font-bold mb-6"
                    ),
                    rx.recharts.bar_chart(
                        rx.recharts.cartesian_grid(
                            stroke_dasharray="3 3", horizontal=True, vertical=False
                        ),
                        rx.recharts.x_axis(
                            data_key="name", type_="category", tick_size=10
                        ),
                        rx.recharts.y_axis(type_="number", domain=[0, 100]),
                        rx.recharts.tooltip(),
                        rx.recharts.bar(
                            data_key="progress_green",
                            stack_id="a",
                            fill="#10b981",
                            name="> 75%",
                        ),
                        rx.recharts.bar(
                            data_key="progress_yellow",
                            stack_id="a",
                            fill="#f59e0b",
                            name="50-75%",
                        ),
                        rx.recharts.bar(
                            data_key="progress_red",
                            stack_id="a",
                            fill="#ef4444",
                            name="< 50%",
                        ),
                        data=MetricasState.gantt_data,
                        width="100%",
                        height=350,
                    ),
                    class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm lg:col-span-2",
                ),
                rx.el.div(
                    rx.el.h3("Salud de Gestión", class_name="text-lg font-bold mb-6"),
                    rx.el.div(
                        rx.foreach(MetricasState.health_indicators, health_card),
                        class_name="flex flex-col gap-3",
                    ),
                    class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.h3("Avances por Etapa", class_name="text-lg font-bold mb-4"),
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
                            rx.foreach(MetricasState.stage_progress, stage_progress_row)
                        ),
                        class_name="min-w-full table-auto border-separate border-spacing-0",
                    ),
                    class_name="overflow-x-auto rounded-xl border border-gray-200",
                ),
                class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "Detalle por Hito Individual", class_name="text-lg font-bold mb-4"
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
                            rx.foreach(MetricasState.milestone_detail, milestone_row)
                        ),
                        class_name="min-w-full table-auto border-separate border-spacing-0",
                    ),
                    class_name="overflow-x-auto rounded-xl border border-gray-200",
                ),
                class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "Exportación de Resultados", class_name="text-lg font-bold mb-4"
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
                        rx.icon("file-spreadsheet", class_name="w-4 h-4 mr-2"),
                        "Auditoría Piezas (0/1)",
                        on_click=MetricasState.export_auditoria,
                        class_name="flex items-center justify-center px-4 py-3 bg-green-50 hover:bg-green-100 text-green-700 font-bold rounded-xl transition-colors",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
                ),
                class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm mb-8",
            ),
            rx.el.div(
                rx.el.h3("Progreso Mensual", class_name="text-lg font-bold mb-6"),
                rx.recharts.bar_chart(
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
                    rx.recharts.x_axis(data_key="month"),
                    rx.recharts.y_axis(),
                    rx.recharts.tooltip(),
                    rx.recharts.bar(
                        data_key="completados", fill="#10b981", radius=[4, 4, 0, 0]
                    ),
                    rx.recharts.bar(
                        data_key="pendientes", fill="#f59e0b", radius=[4, 4, 0, 0]
                    ),
                    data=MetricasState.monthly_progress,
                    width="100%",
                    height=300,
                ),
                class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
            ),
            class_name="max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700",
        ),
        "Métricas",
    )