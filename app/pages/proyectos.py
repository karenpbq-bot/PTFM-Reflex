import reflex as rx
from app.components.navigation import layout
from app.states.proyectos_state import ProyectosState, TimelineStage, ProductData
from app.states.login_state import LoginState


def stage_input(label: str, var_name: str) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-xs font-bold text-gray-500 uppercase tracking-wide mb-1",
        ),
        rx.el.div(
            rx.el.input(
                type="number",
                on_change=lambda val: getattr(ProyectosState, f"set_{var_name}")(val),
                class_name="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm",
                min="0",
                max="100",
                default_value=getattr(ProyectosState, var_name),
            ),
            rx.el.span(
                "%",
                class_name="absolute right-3 top-2.5 text-gray-400 text-sm font-bold",
            ),
            class_name="relative",
        ),
    )


def timeline_row(stage: TimelineStage) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            stage["etapa"], class_name="px-4 py-3 text-sm font-semibold text-gray-800"
        ),
        rx.el.td(stage["inicio"], class_name="px-4 py-3 text-sm text-gray-600"),
        rx.el.td(stage["fin"], class_name="px-4 py-3 text-sm text-gray-600"),
        rx.el.td(
            f"{stage['dias']} días",
            class_name="px-4 py-3 text-sm text-gray-600 font-medium text-right",
        ),
        class_name="border-b border-gray-100 hover:bg-gray-50",
    )


def product_row(prod: ProductData) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            prod["codigo_etiqueta"],
            class_name="px-4 py-3 text-xs font-bold text-blue-600 bg-blue-50/50",
        ),
        rx.el.td(prod["ubicacion"], class_name="px-4 py-3 text-sm text-gray-700"),
        rx.el.td(
            prod["tipo"], class_name="px-4 py-3 text-sm text-gray-700 font-medium"
        ),
        rx.el.td(
            prod["ctd"].to_string(),
            class_name="px-4 py-3 text-sm text-gray-700 text-center",
        ),
        rx.el.td(
            prod["ml"].to_string(),
            class_name="px-4 py-3 text-sm text-gray-700 text-right",
        ),
        rx.el.td(
            rx.el.button(
                rx.icon("pencil", class_name="h-4 w-4"),
                on_click=lambda: ProyectosState.start_edit_product(prod),
                class_name="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors",
            ),
            class_name="px-4 py-3 text-center",
        ),
        class_name="border-b border-gray-100 hover:bg-gray-50",
    )


def tab_registro() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Datos del Proyecto", class_name="text-lg font-bold text-gray-800 mb-4"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Código (Ej: PTF-001)",
                        class_name="block text-sm font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        on_change=ProyectosState.set_reg_codigo,
                        class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                        default_value=ProyectosState.reg_codigo,
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Nombre del Proyecto",
                        class_name="block text-sm font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        on_change=ProyectosState.set_reg_nombre,
                        class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                        default_value=ProyectosState.reg_nombre,
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Cliente",
                        class_name="block text-sm font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        on_change=ProyectosState.set_reg_cliente,
                        class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                        default_value=ProyectosState.reg_cliente,
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Partida",
                        class_name="block text-sm font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        on_change=ProyectosState.set_reg_partida,
                        class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                        default_value=ProyectosState.reg_partida,
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Responsable (Supervisor)",
                        class_name="block text-sm font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("Seleccione responsable...", value=""),
                            rx.foreach(
                                ProyectosState.supervisores,
                                lambda sup: rx.el.option(
                                    sup["nombre"], value=sup["id"].to_string()
                                ),
                            ),
                            value=ProyectosState.reg_responsable,
                            on_change=ProyectosState.set_reg_responsable,
                            class_name="appearance-none w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 bg-white",
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
                        "Fecha Inicio Global",
                        class_name="block text-sm font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="date",
                        on_change=ProyectosState.set_reg_f_ini,
                        class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                        default_value=ProyectosState.reg_f_ini,
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Fecha Término Global",
                        class_name="block text-sm font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="date",
                        on_change=ProyectosState.set_reg_f_fin,
                        class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                        default_value=ProyectosState.reg_f_fin,
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8",
            ),
            class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Distribución de Tiempo por Etapa",
                    class_name="text-lg font-bold text-gray-800",
                ),
                rx.el.div(
                    rx.el.span(
                        "Total: ", class_name="text-sm font-medium text-gray-500"
                    ),
                    rx.el.span(
                        f"{ProyectosState.total_pct}%",
                        class_name=rx.cond(
                            ProyectosState.is_pct_valid,
                            "text-lg font-bold text-green-600",
                            "text-lg font-bold text-red-600",
                        ),
                    ),
                    class_name="bg-gray-50 px-3 py-1 rounded-lg",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.cond(
                ~ProyectosState.is_pct_valid,
                rx.el.p(
                    "La suma de los porcentajes debe ser exactamente 100%.",
                    class_name="text-sm font-bold text-red-500 mb-4",
                ),
                rx.fragment(),
            ),
            rx.el.div(
                stage_input("Diseño", "pct_diseno"),
                stage_input("Fabricación", "pct_fabricacion"),
                stage_input("Traslado", "pct_traslado"),
                stage_input("Instalación", "pct_instalacion"),
                stage_input("Entrega", "pct_entrega"),
                class_name="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6",
            ),
            rx.cond(
                ProyectosState.is_pct_valid
                & (ProyectosState.calculated_timeline.length() > 0),
                rx.el.div(
                    rx.el.h4(
                        "Previsualización del Cronograma",
                        class_name="text-sm font-bold text-gray-500 uppercase tracking-wide mb-3",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Etapa",
                                        class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Inicio",
                                        class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Fin",
                                        class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Duración",
                                        class_name="px-4 py-2 text-right text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                    ),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    ProyectosState.calculated_timeline, timeline_row
                                )
                            ),
                            class_name="w-full table-auto",
                        ),
                        class_name="rounded-xl border border-gray-200 overflow-hidden",
                    ),
                    class_name="mt-6 p-4 bg-blue-50/50 rounded-xl border border-blue-100",
                ),
            ),
            rx.cond(
                ProyectosState.reg_error != "",
                rx.el.p(
                    ProyectosState.reg_error,
                    class_name="text-sm font-bold text-red-500 mt-4",
                ),
                rx.fragment(),
            ),
            rx.cond(
                ProyectosState.reg_message != "",
                rx.el.p(
                    ProyectosState.reg_message,
                    class_name="text-sm font-bold text-green-600 mt-4 bg-green-50 p-3 rounded-lg border border-green-100",
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("save", class_name="h-5 w-5 mr-2"),
                    "Registrar Proyecto",
                    on_click=ProyectosState.save_project,
                    disabled=~ProyectosState.is_pct_valid,
                    class_name="mt-6 w-full md:w-auto flex items-center justify-center px-8 py-3 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm",
                ),
                class_name="flex justify-end",
            ),
            class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
        ),
        class_name="max-w-4xl mx-auto",
    )


def project_list_row(proj: dict) -> rx.Component:
    estatus_color = rx.match(
        proj["estatus"],
        ("Activo", "bg-green-100 text-green-700"),
        ("Pausado", "bg-yellow-100 text-yellow-700"),
        ("Finalizado", "bg-gray-100 text-gray-700"),
        "bg-gray-100 text-gray-600",
    )
    return rx.el.tr(
        rx.el.td(
            proj["codigo"], class_name="px-4 py-3 text-sm font-bold text-blue-600"
        ),
        rx.el.td(
            proj["nombre"], class_name="px-4 py-3 text-sm font-medium text-gray-900"
        ),
        rx.el.td(proj["cliente"], class_name="px-4 py-3 text-sm text-gray-600"),
        rx.el.td(proj["responsable"], class_name="px-4 py-3 text-sm text-gray-600"),
        rx.el.td(
            proj["nro_productos"],
            class_name="px-4 py-3 text-sm text-gray-700 text-center font-medium",
        ),
        rx.el.td(
            proj["avance"],
            class_name="px-4 py-3 text-sm text-gray-700 text-center font-medium",
        ),
        rx.el.td(
            rx.el.span(
                proj["estatus"],
                class_name=f"px-2 py-1 rounded-full text-xs font-bold {estatus_color}",
            ),
            class_name="px-4 py-3",
        ),
        class_name="border-b border-gray-100 hover:bg-gray-50",
    )


def tab_listado() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Listado de Proyectos",
                class_name="text-lg font-bold text-gray-800 mb-4",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Código",
                                class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                            ),
                            rx.el.th(
                                "Nombre",
                                class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                            ),
                            rx.el.th(
                                "Cliente",
                                class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                            ),
                            rx.el.th(
                                "Responsable",
                                class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                            ),
                            rx.el.th(
                                "Productos",
                                class_name="px-4 py-2 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50",
                            ),
                            rx.el.th(
                                "Avance",
                                class_name="px-4 py-2 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50",
                            ),
                            rx.el.th(
                                "Estatus",
                                class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                            ),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            ProyectosState.projects_with_details, project_list_row
                        )
                    ),
                    class_name="w-full table-auto",
                ),
                class_name="overflow-x-auto border border-gray-100 rounded-xl",
            ),
            class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
        )
    )


def edit_product_modal() -> rx.Component:
    return rx.cond(
        ProyectosState.show_edit_product_modal,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Editar Producto", class_name="text-xl font-bold text-gray-900"
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-5 w-5"),
                        on_click=ProyectosState.cancel_edit_product,
                        class_name="text-gray-400 hover:text-gray-600",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Ubicación",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        default_value=ProyectosState.edit_prod_ubicacion,
                        on_change=ProyectosState.set_edit_prod_ubicacion,
                        class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Tipo",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        default_value=ProyectosState.edit_prod_tipo,
                        on_change=ProyectosState.set_edit_prod_tipo,
                        class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Cantidad",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="number",
                            default_value=ProyectosState.edit_prod_ctd.to_string(),
                            on_change=ProyectosState.set_edit_prod_ctd,
                            min="1",
                            class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "ML",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="number",
                            step="0.01",
                            default_value=ProyectosState.edit_prod_ml.to_string(),
                            on_change=ProyectosState.set_edit_prod_ml,
                            min="0",
                            class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=ProyectosState.cancel_edit_product,
                        class_name="px-4 py-2 text-gray-700 font-medium hover:bg-gray-100 rounded-xl transition-colors",
                    ),
                    rx.el.button(
                        "Guardar Cambios",
                        on_click=ProyectosState.save_edit_product,
                        class_name="px-4 py-2 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-colors",
                    ),
                    class_name="flex justify-end gap-3",
                ),
                class_name="bg-white p-8 rounded-2xl w-full max-w-md shadow-2xl",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/40 backdrop-blur-sm p-4",
        ),
        rx.fragment(),
    )


def tab_matriz() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Seleccionar Proyecto",
                class_name="block text-sm font-semibold text-gray-700 mb-1",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("-- Seleccione un proyecto --", value=""),
                    rx.foreach(
                        ProyectosState.projects,
                        lambda p: rx.el.option(
                            f"[{p['codigo']}] {p['nombre']}", value=p["id"]
                        ),
                    ),
                    value=ProyectosState.sel_proj_tab2,
                    on_change=ProyectosState.select_project_tab2,
                    class_name="appearance-none w-full md:w-96 px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 bg-white shadow-sm",
                ),
                rx.icon(
                    "chevron-down",
                    class_name="absolute right-3 top-2.5 h-4 w-4 text-gray-400 pointer-events-none md:right-[calc(100%-23rem)]",
                ),
                class_name="relative",
            ),
            class_name="mb-6 p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
        ),
        rx.cond(
            ProyectosState.sel_proj_tab2 != "",
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon("package", class_name="h-6 w-6 text-blue-500"),
                            class_name="p-3 bg-blue-50 rounded-xl mr-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Total Productos",
                                class_name="text-sm font-semibold text-gray-500",
                            ),
                            rx.el.p(
                                ProyectosState.total_products.to_string(),
                                class_name="text-2xl font-bold text-gray-900",
                            ),
                        ),
                        class_name="flex items-center p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon("ruler", class_name="h-6 w-6 text-purple-500"),
                            class_name="p-3 bg-purple-50 rounded-xl mr-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Total Metraje (ML)",
                                class_name="text-sm font-semibold text-gray-500",
                            ),
                            rx.el.p(
                                ProyectosState.total_metraje,
                                class_name="text-2xl font-bold text-gray-900",
                            ),
                        ),
                        class_name="flex items-center p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Agregar Producto Manual",
                        class_name="text-lg font-bold text-gray-800 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Ubicación",
                                class_name="block text-xs font-bold text-gray-500 uppercase tracking-wide mb-1",
                            ),
                            rx.el.input(
                                on_change=ProyectosState.set_prod_ubicacion,
                                class_name="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm",
                                default_value=ProyectosState.prod_ubicacion,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Tipo",
                                class_name="block text-xs font-bold text-gray-500 uppercase tracking-wide mb-1",
                            ),
                            rx.el.input(
                                on_change=ProyectosState.set_prod_tipo,
                                class_name="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm",
                                default_value=ProyectosState.prod_tipo,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Cantidad",
                                class_name="block text-xs font-bold text-gray-500 uppercase tracking-wide mb-1",
                            ),
                            rx.el.input(
                                type="number",
                                on_change=ProyectosState.set_prod_ctd,
                                min="1",
                                class_name="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm",
                                default_value=ProyectosState.prod_ctd,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "ML",
                                class_name="block text-xs font-bold text-gray-500 uppercase tracking-wide mb-1",
                            ),
                            rx.el.input(
                                type="number",
                                step="0.01",
                                on_change=ProyectosState.set_prod_ml,
                                min="0",
                                class_name="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm",
                                default_value=ProyectosState.prod_ml,
                            ),
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Agregar",
                                on_click=ProyectosState.add_manual_product,
                                class_name="w-full h-[38px] mt-6 bg-gray-900 text-white text-sm font-bold rounded-lg hover:bg-black transition-colors",
                            )
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-5 gap-4 items-start",
                    ),
                    class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm mb-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Importar desde Excel",
                        class_name="text-lg font-bold text-gray-800 mb-2",
                    ),
                    rx.el.p(
                        "El archivo debe contener las columnas: UBICACION, TIPO, CTD, Medidas (ml)",
                        class_name="text-sm text-gray-500 mb-4",
                    ),
                    rx.upload.root(
                        rx.el.div(
                            rx.icon(
                                "cloud_upload", class_name="h-8 w-8 text-gray-400 mb-2"
                            ),
                            rx.el.p(
                                "Arrastra o haz clic para subir archivo .xlsx",
                                class_name="text-sm font-semibold text-gray-600",
                            ),
                            class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed border-gray-300 rounded-xl hover:border-blue-500 hover:bg-blue-50 transition-colors cursor-pointer",
                        ),
                        id="excel_upload",
                        accept={
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
                                ".xlsx"
                            ],
                            "application/vnd.ms-excel": [".xls"],
                        },
                        on_drop=ProyectosState.handle_excel_upload,
                        max_files=1,
                    ),
                    class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm mb-6",
                ),
                rx.cond(
                    ProyectosState.matriz_error != "",
                    rx.el.p(
                        ProyectosState.matriz_error,
                        class_name="text-sm font-bold text-red-500 mb-4",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    ProyectosState.matriz_message != "",
                    rx.el.p(
                        ProyectosState.matriz_message,
                        class_name="text-sm font-bold text-green-600 mb-4 bg-green-50 p-3 rounded-lg border border-green-100",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Listado de Productos",
                            class_name="text-lg font-bold text-gray-800",
                        ),
                        rx.el.button(
                            rx.icon("trash-2", class_name="h-4 w-4 mr-2"),
                            "Vaciar Matriz",
                            on_click=ProyectosState.vaciar_matriz,
                            class_name="flex items-center px-4 py-2 text-sm font-bold text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors",
                        ),
                        class_name="flex justify-between items-center mb-4",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Código Etiqueta",
                                        class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Ubicación",
                                        class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Tipo",
                                        class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Cantidad",
                                        class_name="px-4 py-2 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "ML",
                                        class_name="px-4 py-2 text-right text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Acciones",
                                        class_name="px-4 py-2 text-center text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                    ),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(ProyectosState.products_tab2, product_row)
                            ),
                            class_name="w-full table-auto",
                        ),
                        class_name="overflow-x-auto border border-gray-100 rounded-xl",
                    ),
                    class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
                ),
            ),
        ),
    )


def tab_gestion() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Seleccionar Proyecto a Editar",
                class_name="block text-sm font-semibold text-gray-700 mb-1",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("-- Seleccione un proyecto --", value=""),
                    rx.foreach(
                        ProyectosState.projects,
                        lambda p: rx.el.option(
                            f"[{p['codigo']}] {p['nombre']}", value=p["id"]
                        ),
                    ),
                    value=ProyectosState.sel_proj_tab3,
                    on_change=ProyectosState.select_project_tab3,
                    class_name="appearance-none w-full md:w-96 px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 bg-white shadow-sm",
                ),
                rx.icon(
                    "chevron-down",
                    class_name="absolute right-3 top-2.5 h-4 w-4 text-gray-400 pointer-events-none md:right-[calc(100%-23rem)]",
                ),
                class_name="relative",
            ),
            class_name="mb-6 p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
        ),
        rx.cond(
            ProyectosState.sel_proj_tab3 != "",
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Editar Información",
                        class_name="text-lg font-bold text-gray-800 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Nombre del Proyecto",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                on_change=ProyectosState.set_edit_nombre,
                                class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                                default_value=ProyectosState.edit_nombre,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Cliente",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                on_change=ProyectosState.set_edit_cliente,
                                class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                                default_value=ProyectosState.edit_cliente,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Partida",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                on_change=ProyectosState.set_edit_partida,
                                class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500",
                                default_value=ProyectosState.edit_partida,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Estatus",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option("Activo", value="Activo"),
                                    rx.el.option("Pausado", value="Pausado"),
                                    rx.el.option("Finalizado", value="Finalizado"),
                                    value=ProyectosState.edit_estatus,
                                    on_change=ProyectosState.set_edit_estatus,
                                    class_name="appearance-none w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 bg-white",
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
                                "Responsable",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option("Sin responsable", value=""),
                                    rx.foreach(
                                        ProyectosState.supervisores,
                                        lambda sup: rx.el.option(
                                            sup["nombre"], value=sup["id"].to_string()
                                        ),
                                    ),
                                    value=ProyectosState.edit_responsable,
                                    on_change=ProyectosState.set_edit_responsable,
                                    class_name="appearance-none w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 bg-white",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="absolute right-3 top-2.5 h-4 w-4 text-gray-400 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                            class_name="md:col-span-2",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                    ),
                    rx.cond(
                        ProyectosState.edit_error != "",
                        rx.el.p(
                            ProyectosState.edit_error,
                            class_name="text-sm font-bold text-red-500 mb-4",
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        ProyectosState.edit_message != "",
                        rx.el.p(
                            ProyectosState.edit_message,
                            class_name="text-sm font-bold text-green-600 mb-4 bg-green-50 p-3 rounded-lg border border-green-100",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Guardar Cambios",
                            on_click=ProyectosState.update_project,
                            class_name="px-6 py-2 bg-gray-900 text-white font-bold rounded-xl hover:bg-black transition-colors shadow-sm",
                        ),
                        class_name="flex justify-end",
                    ),
                    class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Zona de Peligro",
                            class_name="text-lg font-bold text-red-600",
                        ),
                        rx.el.p(
                            "Esta acción eliminará permanentemente el proyecto y TODOS sus registros asociados (Productos, Seguimientos, Incidencias).",
                            class_name="text-sm text-gray-600 mt-1",
                        ),
                    ),
                    rx.radix.primitives.dialog.root(
                        rx.radix.primitives.dialog.trigger(
                            rx.el.button(
                                "Eliminar Proyecto Completo",
                                class_name="px-6 py-2 bg-red-100 text-red-700 font-bold rounded-xl hover:bg-red-200 transition-colors",
                            )
                        ),
                        rx.radix.primitives.dialog.portal(
                            rx.radix.primitives.dialog.overlay(
                                class_name="fixed inset-0 bg-black/50 z-50"
                            ),
                            rx.radix.primitives.dialog.content(
                                rx.el.div(
                                    rx.el.h2(
                                        "¿Está absolutamente seguro?",
                                        class_name="text-xl font-bold text-gray-900 mb-2",
                                    ),
                                    rx.el.p(
                                        "Esta acción no se puede deshacer. Se eliminarán los productos y todo el historial del proyecto.",
                                        class_name="text-gray-600 mb-6",
                                    ),
                                    rx.el.div(
                                        rx.radix.primitives.dialog.close(
                                            rx.el.button(
                                                "Cancelar",
                                                class_name="px-4 py-2 text-gray-600 font-medium hover:bg-gray-100 rounded-lg",
                                            )
                                        ),
                                        rx.radix.primitives.dialog.close(
                                            rx.el.button(
                                                "Sí, eliminar",
                                                on_click=ProyectosState.delete_project_full,
                                                class_name="px-4 py-2 bg-red-600 text-white font-bold rounded-lg hover:bg-red-700",
                                            )
                                        ),
                                        class_name="flex justify-end gap-3",
                                    ),
                                    class_name="bg-white p-6 rounded-2xl shadow-xl w-[90vw] max-w-md mx-auto relative top-1/2 -translate-y-1/2",
                                ),
                                class_name="fixed inset-0 z-50 overflow-y-auto",
                            ),
                        ),
                    ),
                    class_name="p-6 bg-red-50/50 border border-red-100 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4",
                ),
            ),
        ),
    )


def proyectos_page() -> rx.Component:
    return layout(
        rx.el.div(
            edit_product_modal(),
            rx.cond(
                LoginState.user_role == "Supervisor",
                supervisor_view_content(),
                admin_view_content(),
            ),
            class_name="max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700",
        ),
        "Proyectos",
    )


def supervisor_view_content() -> rx.Component:
    return rx.radix.tabs.root(
        rx.radix.tabs.list(
            rx.radix.tabs.trigger(
                rx.el.span(
                    "📋 Listado de Proyectos", class_name="flex items-center gap-2"
                ),
                value="tab_listado",
                class_name="px-4 py-2 font-semibold text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 outline-none",
            ),
            class_name="flex gap-4 border-b border-gray-200 mb-6",
        ),
        rx.radix.tabs.content(
            tab_listado(), value="tab_listado", class_name="outline-none"
        ),
        default_value="tab_listado",
    )


def admin_view_content() -> rx.Component:
    return rx.radix.tabs.root(
        rx.radix.tabs.list(
            rx.radix.tabs.trigger(
                rx.el.span(
                    "📋 Listado de Proyectos", class_name="flex items-center gap-2"
                ),
                value="tab_listado",
                class_name="px-4 py-2 font-semibold text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 outline-none",
            ),
            rx.radix.tabs.trigger(
                rx.el.span(
                    "🆕 Registrar Proyecto", class_name="flex items-center gap-2"
                ),
                value="tab1",
                class_name="px-4 py-2 font-semibold text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 outline-none",
            ),
            rx.radix.tabs.trigger(
                rx.el.span(
                    "📦 Matriz de Productos", class_name="flex items-center gap-2"
                ),
                value="tab2",
                class_name="px-4 py-2 font-semibold text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 outline-none",
            ),
            rx.radix.tabs.trigger(
                rx.el.span("⚙️ Gestión y Edición", class_name="flex items-center gap-2"),
                value="tab3",
                class_name="px-4 py-2 font-semibold text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 outline-none",
            ),
            class_name="flex gap-4 border-b border-gray-200 mb-6",
        ),
        rx.radix.tabs.content(
            tab_listado(), value="tab_listado", class_name="outline-none"
        ),
        rx.radix.tabs.content(tab_registro(), value="tab1", class_name="outline-none"),
        rx.radix.tabs.content(tab_matriz(), value="tab2", class_name="outline-none"),
        rx.radix.tabs.content(tab_gestion(), value="tab3", class_name="outline-none"),
        default_value="tab_listado",
    )