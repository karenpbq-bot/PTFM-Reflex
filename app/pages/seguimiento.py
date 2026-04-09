import reflex as rx
from app.components.navigation import layout
from app.states.seguimiento_state import SeguimientoState, SeguimientoProduct
from app.states.login_state import LoginState


def milestone_cell(
    product: SeguimientoProduct, idx: int, hito_name: str
) -> rx.Component:
    check_key = product["id"].to_string() + "_" + hito_name
    return rx.el.td(
        rx.el.button(
            rx.cond(
                SeguimientoState.delete_pending.contains(check_key),
                rx.icon("x", class_name="h-4 w-4 text-white"),
                rx.cond(
                    SeguimientoState.db_checks.contains(check_key),
                    rx.icon("check", class_name="h-4 w-4 text-white"),
                    rx.cond(
                        SeguimientoState.pending_checks.contains(check_key),
                        rx.icon("check", class_name="h-4 w-4 text-white"),
                        None,
                    ),
                ),
            ),
            on_click=lambda: SeguimientoState.toggle_check(
                product["id"].to_string(), idx
            ),
            class_name=rx.cond(
                SeguimientoState.delete_pending.contains(check_key),
                "h-8 w-8 rounded-lg bg-yellow-500 flex items-center justify-center transition-all hover:bg-yellow-600 shadow-sm",
                rx.cond(
                    SeguimientoState.db_checks.contains(check_key),
                    "h-8 w-8 rounded-lg bg-gray-400 flex items-center justify-center transition-all hover:bg-gray-500 shadow-sm",
                    rx.cond(
                        SeguimientoState.pending_checks.contains(check_key),
                        "h-8 w-8 rounded-lg bg-red-500 flex items-center justify-center transition-all hover:bg-red-600 shadow-sm animate-pulse",
                        "h-6 w-6 rounded-lg bg-red-500/50 flex items-center justify-center transition-all hover:bg-red-500 shadow-sm mx-auto",
                    ),
                ),
            ),
        ),
        class_name="px-4 py-2 text-center align-middle",
    )


def product_row(product: SeguimientoProduct) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            product["codigo_etiqueta"],
            class_name="px-4 py-3 text-sm font-semibold text-gray-900 border-b border-gray-100 sticky left-0 bg-white z-10 whitespace-nowrap",
        ),
        rx.el.td(
            product["ubicacion"],
            class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100 whitespace-nowrap",
        ),
        rx.el.td(
            product["tipo"],
            class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100 whitespace-nowrap",
        ),
        rx.el.td(
            product["ml"].to_string(),
            class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100 whitespace-nowrap text-right",
        ),
        rx.el.td(
            product["ctd"].to_string(),
            class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100 whitespace-nowrap text-center",
        ),
        milestone_cell(product, 0, "Diseñado"),
        milestone_cell(product, 1, "Fabricado"),
        milestone_cell(product, 2, "Material en Obra"),
        milestone_cell(product, 3, "Material en Ubicación"),
        milestone_cell(product, 4, "Instalación de Estructura"),
        milestone_cell(product, 5, "Instalación de Puertas o Frentes"),
        milestone_cell(product, 6, "Revisión y Observaciones"),
        milestone_cell(product, 7, "Entrega"),
        class_name="hover:bg-gray-50 transition-colors",
    )


def seguimiento_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Selección de Proyecto",
                class_name="text-lg font-bold text-gray-800 mb-4",
            ),
            rx.el.div(
                rx.el.input(
                    placeholder="Buscar proyecto...",
                    on_change=SeguimientoState.set_search_text.debounce(500),
                    class_name="w-full md:w-1/3 px-4 py-2 border border-gray-200 rounded-lg",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("-- Seleccione un Proyecto --", value=""),
                        rx.foreach(
                            SeguimientoState.projects_list,
                            lambda p: rx.el.option(p["label"], value=p["id"]),
                        ),
                        value=SeguimientoState.selected_project_id,
                        on_change=SeguimientoState.select_project,
                        class_name="appearance-none w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="absolute right-3 top-2.5 h-4 w-4 text-gray-400 pointer-events-none",
                    ),
                    class_name="relative w-full md:w-2/3",
                ),
                class_name="flex flex-col md:flex-row gap-4",
            ),
            class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm mb-6",
        ),
        rx.cond(
            SeguimientoState.selected_project_id != "",
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Avance Total",
                            class_name="text-sm text-gray-500 font-bold uppercase",
                        ),
                        rx.el.p(
                            f"{SeguimientoState.avance_total}%",
                            class_name="text-3xl font-black text-blue-600 mt-1",
                        ),
                        class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm flex-1",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Avance de Selección",
                            class_name="text-sm text-gray-500 font-bold uppercase",
                        ),
                        rx.el.p(
                            f"{SeguimientoState.avance_seleccion}%",
                            class_name="text-3xl font-black text-green-600 mt-1",
                        ),
                        class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm flex-1",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.select(
                                rx.el.option("Sin grupo", value="none"),
                                rx.el.option("Ubicación", value="ubicacion"),
                                rx.el.option("Tipo", value="tipo"),
                                on_change=SeguimientoState.set_group_by,
                                value=SeguimientoState.group_by,
                                class_name="appearance-none w-full px-4 py-2 border border-gray-200 rounded-lg bg-white",
                            ),
                            rx.icon(
                                "chevron-down",
                                class_name="absolute right-3 top-2.5 h-4 w-4 text-gray-400 pointer-events-none",
                            ),
                            class_name="relative flex-1",
                        ),
                        rx.el.input(
                            placeholder="Búsqueda Principal...",
                            on_change=SeguimientoState.set_primary_filter.debounce(500),
                            class_name="flex-1 px-4 py-2 border border-gray-200 rounded-lg",
                        ),
                        rx.el.input(
                            placeholder="Refinar Búsqueda...",
                            on_change=SeguimientoState.set_refinement_filter.debounce(
                                500
                            ),
                            class_name="flex-1 px-4 py-2 border border-gray-200 rounded-lg",
                        ),
                        class_name="flex flex-col md:flex-row gap-4 mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Guardar Marcación",
                            class_name="px-4 py-2 bg-gray-500 text-white font-bold rounded-lg hover:bg-gray-600 transition-colors",
                        ),
                        rx.el.button(
                            "🚀 Guardar Avance",
                            on_click=SeguimientoState.guardar_avance,
                            class_name="px-4 py-2 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition-colors",
                        ),
                        rx.el.button(
                            "Limpiar Marcación",
                            on_click=SeguimientoState.limpiar_marcacion,
                            class_name="px-4 py-2 bg-gray-200 text-gray-700 font-bold rounded-lg hover:bg-gray-300 transition-colors",
                        ),
                        rx.cond(
                            SeguimientoState.is_jefe,
                            rx.el.button(
                                "Borrar Avance",
                                on_click=SeguimientoState.borrar_avance,
                                class_name="px-4 py-2 bg-red-500 text-white font-bold rounded-lg hover:bg-red-600 transition-colors",
                            ),
                        ),
                        rx.el.div(
                            rx.upload.root(
                                rx.el.div(
                                    rx.icon("upload", class_name="h-4 w-4 mr-2"),
                                    rx.el.span(
                                        "Importar Avance",
                                        class_name="text-sm font-bold",
                                    ),
                                    class_name="flex items-center justify-center px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors cursor-pointer",
                                ),
                                id="import_seguimiento",
                                accept={
                                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
                                        ".xlsx"
                                    ],
                                    "application/vnd.ms-excel": [".xls"],
                                },
                                on_drop=SeguimientoState.handle_import_seguimiento,
                                max_files=1,
                            ),
                            class_name="inline-block",
                        ),
                        rx.el.button(
                            "Exportar Avance",
                            on_click=SeguimientoState.export_seguimiento,
                            class_name="px-4 py-2 bg-green-500 text-white font-bold rounded-lg hover:bg-green-600 transition-colors",
                        ),
                        class_name="flex flex-wrap gap-4",
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm mb-6",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Código",
                                    class_name="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200 sticky left-0 z-20 whitespace-nowrap",
                                ),
                                rx.el.th(
                                    "Ubicación",
                                    class_name="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200 whitespace-nowrap",
                                ),
                                rx.el.th(
                                    "Tipo",
                                    class_name="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200 whitespace-nowrap",
                                ),
                                rx.el.th(
                                    "ML",
                                    class_name="px-4 py-3 text-right text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200 whitespace-nowrap",
                                ),
                                rx.el.th(
                                    "Ctd",
                                    class_name="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50 border-b border-gray-200 whitespace-nowrap",
                                ),
                                rx.el.th(
                                    "🗺️",
                                    class_name="px-4 py-3 text-center text-lg bg-gray-50 border-b border-gray-200",
                                ),
                                rx.el.th(
                                    "🪚",
                                    class_name="px-4 py-3 text-center text-lg bg-gray-50 border-b border-gray-200",
                                ),
                                rx.el.th(
                                    "🚛",
                                    class_name="px-4 py-3 text-center text-lg bg-gray-50 border-b border-gray-200",
                                ),
                                rx.el.th(
                                    "📍",
                                    class_name="px-4 py-3 text-center text-lg bg-gray-50 border-b border-gray-200",
                                ),
                                rx.el.th(
                                    "📦",
                                    class_name="px-4 py-3 text-center text-lg bg-gray-50 border-b border-gray-200",
                                ),
                                rx.el.th(
                                    "🗄️",
                                    class_name="px-4 py-3 text-center text-lg bg-gray-50 border-b border-gray-200",
                                ),
                                rx.el.th(
                                    "🔍",
                                    class_name="px-4 py-3 text-center text-lg bg-gray-50 border-b border-gray-200",
                                ),
                                rx.el.th(
                                    "👍",
                                    class_name="px-4 py-3 text-center text-lg bg-gray-50 border-b border-gray-200",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(SeguimientoState.filtered_products, product_row),
                            class_name="bg-white divide-y divide-gray-100",
                        ),
                        class_name="min-w-full table-auto border-separate border-spacing-0",
                    ),
                    class_name="overflow-x-auto bg-white rounded-2xl border border-gray-200 shadow-sm max-h-[600px]",
                ),
            ),
        ),
        class_name="max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700",
    )


def seguimiento_page() -> rx.Component:
    return layout(
        seguimiento_content(),
        rx.cond(
            SeguimientoState.selected_project_label != "",
            f"Seguimiento: {SeguimientoState.selected_project_label}",
            "Seguimiento de Proyectos",
        ),
    )