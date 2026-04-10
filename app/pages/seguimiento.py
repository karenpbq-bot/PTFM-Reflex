import reflex as rx
from app.components.navigation import layout
from app.states.seguimiento_state import SeguimientoState, SeguimientoProduct
from app.states.login_state import LoginState


def milestone_cell(product: SeguimientoProduct, idx: int) -> rx.Component:
    check_key = f"{product['id'].to_string()}_{idx}"
    cell_status = SeguimientoState.cell_statuses.get(check_key, "empty")
    return rx.el.td(
        rx.el.button(
            rx.match(
                cell_status,
                ("delete_pending", rx.icon("x", class_name="h-4 w-4 text-white")),
                ("saved", rx.icon("check", class_name="h-4 w-4 text-white")),
                ("pending", rx.icon("check", class_name="h-4 w-4 text-white")),
                rx.fragment(),
            ),
            on_click=lambda: SeguimientoState.toggle_check(
                product["id"].to_string(), idx
            ),
            class_name=SeguimientoState.cell_colors.get(
                check_key,
                "h-6 w-6 rounded-lg bg-gray-200 flex items-center justify-center transition-all hover:bg-blue-400 shadow-sm mx-auto",
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
        milestone_cell(product, 0),
        milestone_cell(product, 1),
        milestone_cell(product, 2),
        milestone_cell(product, 3),
        milestone_cell(product, 4),
        milestone_cell(product, 5),
        milestone_cell(product, 6),
        milestone_cell(product, 7),
        rx.el.td(
            rx.el.input(
                default_value=SeguimientoState.product_notes.get(
                    product["id"].to_string(), ""
                ),
                on_change=lambda val: SeguimientoState.set_product_note(
                    product["id"].to_string(), val
                ),
                placeholder="...",
                class_name="w-24 px-2 py-1 text-xs border border-gray-200 rounded focus:ring-1 focus:ring-blue-400 focus:border-blue-400 bg-transparent",
            ),
            class_name="px-2 py-2 border-b border-gray-100",
        ),
        class_name="hover:bg-gray-50 transition-colors",
    )


def seguimiento_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.el.div(
                    rx.icon("folder-search", class_name="h-5 w-5 text-blue-600"),
                    rx.el.span(
                        "Selección de Proyecto",
                        class_name="text-lg font-bold text-gray-800",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.icon(
                    rx.cond(
                        SeguimientoState.show_project_selector,
                        "chevron-up",
                        "chevron-down",
                    ),
                    class_name="h-5 w-5 text-gray-400",
                ),
                on_click=SeguimientoState.toggle_project_selector,
                class_name="flex items-center justify-between w-full p-4 hover:bg-gray-50 rounded-t-2xl transition-colors",
            ),
            rx.cond(
                SeguimientoState.show_project_selector,
                rx.el.div(
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
                    class_name="px-4 pb-4",
                ),
            ),
            class_name="bg-white rounded-2xl border border-gray-200 shadow-sm mb-6",
        ),
        rx.el.div(
            rx.el.button(
                rx.el.div(
                    rx.icon("settings", class_name="h-5 w-5 text-gray-600"),
                    rx.el.span(
                        "Configuraciones Avanzadas",
                        class_name="text-lg font-bold text-gray-800",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.icon(
                    rx.cond(
                        SeguimientoState.show_advanced_config,
                        "chevron-up",
                        "chevron-down",
                    ),
                    class_name="h-5 w-5 text-gray-400",
                ),
                on_click=SeguimientoState.toggle_advanced_config,
                class_name="flex items-center justify-between w-full p-4 hover:bg-gray-50 rounded-t-2xl transition-colors",
            ),
            rx.cond(
                SeguimientoState.show_advanced_config,
                rx.el.div(
                    rx.radix.tabs.root(
                        rx.radix.tabs.list(
                            rx.radix.tabs.trigger(
                                "🔍 Filtros",
                                value="filtros",
                                class_name="px-4 py-2 font-semibold text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 outline-none",
                            ),
                            rx.radix.tabs.trigger(
                                "⚖️ Ponderación",
                                value="ponderacion",
                                class_name="px-4 py-2 font-semibold text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 outline-none",
                            ),
                            rx.radix.tabs.trigger(
                                "📥 Importación",
                                value="importacion",
                                class_name="px-4 py-2 font-semibold text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 outline-none",
                            ),
                            class_name="flex gap-2 border-b border-gray-200 mb-4",
                        ),
                        rx.radix.tabs.content(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.label(
                                            "Agrupar por:",
                                            class_name="block text-xs font-bold text-gray-500 uppercase tracking-wide mb-1",
                                        ),
                                        rx.el.div(
                                            rx.el.select(
                                                rx.el.option("Sin grupo", value="none"),
                                                rx.el.option(
                                                    "Ubicación", value="ubicacion"
                                                ),
                                                rx.el.option("Tipo", value="tipo"),
                                                rx.el.option(
                                                    "Sin avance (todos vacíos)",
                                                    value="sin_avance",
                                                ),
                                                rx.el.option(
                                                    "Sin Diseñado", value="sin_hito_0"
                                                ),
                                                rx.el.option(
                                                    "Sin Fabricado", value="sin_hito_1"
                                                ),
                                                rx.el.option(
                                                    "Sin Material en Obra",
                                                    value="sin_hito_2",
                                                ),
                                                rx.el.option(
                                                    "Sin Material en Ubicación",
                                                    value="sin_hito_3",
                                                ),
                                                rx.el.option(
                                                    "Sin Inst. Estructura",
                                                    value="sin_hito_4",
                                                ),
                                                rx.el.option(
                                                    "Sin Inst. Puertas/Frentes",
                                                    value="sin_hito_5",
                                                ),
                                                rx.el.option(
                                                    "Sin Revisión", value="sin_hito_6"
                                                ),
                                                rx.el.option(
                                                    "Sin Entrega", value="sin_hito_7"
                                                ),
                                                on_change=SeguimientoState.set_group_by,
                                                value=SeguimientoState.group_by,
                                                class_name="appearance-none w-full px-4 py-2 border border-gray-200 rounded-lg bg-white",
                                            ),
                                            rx.icon(
                                                "chevron-down",
                                                class_name="absolute right-3 top-2.5 h-4 w-4 text-gray-400 pointer-events-none",
                                            ),
                                            class_name="relative",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            "Búsqueda Principal:",
                                            class_name="block text-xs font-bold text-gray-500 uppercase tracking-wide mb-1",
                                        ),
                                        rx.el.input(
                                            placeholder="Código, ubicación o tipo...",
                                            on_change=SeguimientoState.set_primary_filter.debounce(
                                                500
                                            ),
                                            class_name="w-full px-4 py-2 border border-gray-200 rounded-lg",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            "Refinar Búsqueda:",
                                            class_name="block text-xs font-bold text-gray-500 uppercase tracking-wide mb-1",
                                        ),
                                        rx.el.input(
                                            placeholder="Segundo filtro...",
                                            on_change=SeguimientoState.set_refinement_filter.debounce(
                                                500
                                            ),
                                            class_name="w-full px-4 py-2 border border-gray-200 rounded-lg",
                                        ),
                                    ),
                                    class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
                                )
                            ),
                            value="filtros",
                            class_name="outline-none",
                        ),
                        rx.radix.tabs.content(
                            rx.el.div(
                                rx.el.p(
                                    "Asigne el peso porcentual de cada hito para el cálculo del avance. La suma debe ser 100%.",
                                    class_name="text-sm text-gray-500 mb-4",
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.label(
                                            "🗺️ Diseñado",
                                            class_name="block text-xs font-bold text-gray-600 mb-1",
                                        ),
                                        rx.el.input(
                                            type="number",
                                            default_value="15",
                                            on_change=lambda v: SeguimientoState.set_milestone_weight(
                                                "Diseñado", v
                                            ),
                                            min="0",
                                            max="100",
                                            class_name="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm text-center",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            "🪚 Fabricado",
                                            class_name="block text-xs font-bold text-gray-600 mb-1",
                                        ),
                                        rx.el.input(
                                            type="number",
                                            default_value="40",
                                            on_change=lambda v: SeguimientoState.set_milestone_weight(
                                                "Fabricado", v
                                            ),
                                            min="0",
                                            max="100",
                                            class_name="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm text-center",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            "🚛 Material en Obra",
                                            class_name="block text-xs font-bold text-gray-600 mb-1",
                                        ),
                                        rx.el.input(
                                            type="number",
                                            default_value="5",
                                            on_change=lambda v: SeguimientoState.set_milestone_weight(
                                                "Material en Obra", v
                                            ),
                                            min="0",
                                            max="100",
                                            class_name="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm text-center",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            "📍 Material en Ubicación",
                                            class_name="block text-xs font-bold text-gray-600 mb-1",
                                        ),
                                        rx.el.input(
                                            type="number",
                                            default_value="5",
                                            on_change=lambda v: SeguimientoState.set_milestone_weight(
                                                "Material en Ubicación", v
                                            ),
                                            min="0",
                                            max="100",
                                            class_name="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm text-center",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            "📦 Inst. Estructura",
                                            class_name="block text-xs font-bold text-gray-600 mb-1",
                                        ),
                                        rx.el.input(
                                            type="number",
                                            default_value="15",
                                            on_change=lambda v: SeguimientoState.set_milestone_weight(
                                                "Instalación de Estructura", v
                                            ),
                                            min="0",
                                            max="100",
                                            class_name="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm text-center",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            "🗄️ Inst. Puertas",
                                            class_name="block text-xs font-bold text-gray-600 mb-1",
                                        ),
                                        rx.el.input(
                                            type="number",
                                            default_value="10",
                                            on_change=lambda v: SeguimientoState.set_milestone_weight(
                                                "Instalación de Puertas o Frentes", v
                                            ),
                                            min="0",
                                            max="100",
                                            class_name="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm text-center",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            "🔍 Revisión",
                                            class_name="block text-xs font-bold text-gray-600 mb-1",
                                        ),
                                        rx.el.input(
                                            type="number",
                                            default_value="5",
                                            on_change=lambda v: SeguimientoState.set_milestone_weight(
                                                "Revisión y Observaciones", v
                                            ),
                                            min="0",
                                            max="100",
                                            class_name="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm text-center",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            "👍 Entrega",
                                            class_name="block text-xs font-bold text-gray-600 mb-1",
                                        ),
                                        rx.el.input(
                                            type="number",
                                            default_value="5",
                                            on_change=lambda v: SeguimientoState.set_milestone_weight(
                                                "Entrega", v
                                            ),
                                            min="0",
                                            max="100",
                                            class_name="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm text-center",
                                        ),
                                    ),
                                    class_name="grid grid-cols-2 md:grid-cols-4 gap-4",
                                ),
                            ),
                            value="ponderacion",
                            class_name="outline-none",
                        ),
                        rx.radix.tabs.content(
                            rx.el.div(
                                rx.el.p(
                                    "Sube un archivo Excel (.xlsx) con la misma estructura que el archivo exportado. Solo se actualizarán las casillas vacías; los datos existentes se conservan.",
                                    class_name="text-sm text-gray-500 mb-4",
                                ),
                                rx.upload.root(
                                    rx.el.div(
                                        rx.icon(
                                            "cloud_upload",
                                            class_name="h-8 w-8 text-gray-400 mb-2",
                                        ),
                                        rx.el.p(
                                            "Arrastra o haz clic para subir archivo .xlsx",
                                            class_name="text-sm font-semibold text-gray-600",
                                        ),
                                        rx.el.p(
                                            "Solo se actualizan casillas vacías",
                                            class_name="text-xs text-gray-400 mt-1",
                                        ),
                                        class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed border-gray-300 rounded-xl hover:border-purple-500 hover:bg-purple-50 transition-colors cursor-pointer",
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
                            ),
                            value="importacion",
                            class_name="outline-none",
                        ),
                        default_value="filtros",
                    ),
                    class_name="px-4 pb-4",
                ),
            ),
            class_name="bg-white rounded-2xl border border-gray-200 shadow-sm mb-6",
        ),
        rx.cond(
            SeguimientoState.selected_project_id != "",
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "Avance Total",
                            class_name="text-xs text-gray-500 font-bold uppercase",
                        ),
                        rx.el.span(
                            f"{SeguimientoState.avance_total}%",
                            class_name="text-lg font-black text-blue-600 ml-2",
                        ),
                        class_name="flex items-center gap-1 px-4 py-2 bg-white rounded-xl border border-gray-200 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Avance Selección",
                            class_name="text-xs text-gray-500 font-bold uppercase",
                        ),
                        rx.el.span(
                            f"{SeguimientoState.avance_seleccion}%",
                            class_name="text-lg font-black text-green-600 ml-2",
                        ),
                        class_name="flex items-center gap-1 px-4 py-2 bg-white rounded-xl border border-gray-200 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Productos Filtrados",
                            class_name="text-xs text-gray-500 font-bold uppercase",
                        ),
                        rx.el.span(
                            SeguimientoState.filtered_count.to_string(),
                            class_name="text-lg font-black text-gray-800 ml-2",
                        ),
                        class_name="flex items-center gap-1 px-4 py-2 bg-white rounded-xl border border-gray-200 shadow-sm",
                    ),
                    class_name="flex flex-wrap gap-3 mb-4",
                ),
                rx.el.div(
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
                        rx.el.button(
                            "Exportar Avance",
                            on_click=SeguimientoState.export_seguimiento,
                            class_name="px-4 py-2 bg-green-500 text-white font-bold rounded-lg hover:bg-green-600 transition-colors",
                        ),
                        class_name="flex flex-wrap gap-3",
                    ),
                    class_name="bg-white p-4 rounded-2xl border border-gray-200 shadow-sm mb-6",
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
                                rx.el.th(
                                    "📝",
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