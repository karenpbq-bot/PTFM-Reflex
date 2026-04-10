import reflex as rx
from app.components.navigation import layout
from app.states.incidencias_state import (
    IncidenciasState,
    TmpPieza,
    TmpMaterial,
    IncidenciaHistorialItem,
    ProjectSelectorItem,
)


def pieza_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Descripción",
                    class_name="block text-sm font-semibold text-gray-700 mb-1",
                ),
                rx.el.input(
                    on_change=IncidenciasState.set_pz_descripcion,
                    class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                    default_value=IncidenciasState.pz_descripcion,
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Cantidad",
                    class_name="block text-sm font-semibold text-gray-700 mb-1",
                ),
                rx.el.input(
                    type="number",
                    on_change=IncidenciasState.set_pz_cantidad,
                    class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                    default_value=IncidenciasState.pz_cantidad.to_string(),
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Ubicación",
                    class_name="block text-sm font-semibold text-gray-700 mb-1",
                ),
                rx.el.input(
                    on_change=IncidenciasState.set_pz_ubicacion,
                    class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                    default_value=IncidenciasState.pz_ubicacion,
                ),
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Material/Color",
                    class_name="block text-sm font-semibold text-gray-700 mb-1",
                ),
                rx.el.input(
                    on_change=IncidenciasState.set_pz_material,
                    class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                    default_value=IncidenciasState.pz_material,
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Rotación",
                    class_name="block text-sm font-semibold text-gray-700 mb-1",
                ),
                rx.el.input(
                    type="number",
                    on_change=IncidenciasState.set_pz_rotacion,
                    class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                    default_value=IncidenciasState.pz_rotacion.to_string(),
                ),
            ),
            rx.el.div(),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4",
        ),
        rx.el.h4(
            "Dimensiones Críticas",
            class_name="text-sm font-bold text-gray-800 mb-2 mt-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Veta", class_name="block text-sm font-semibold text-gray-700 mb-1"
                ),
                rx.el.input(
                    type="number",
                    step="0.01",
                    on_change=IncidenciasState.set_pz_veta,
                    class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                    default_value=IncidenciasState.pz_veta.to_string(),
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "No Veta",
                    class_name="block text-sm font-semibold text-gray-700 mb-1",
                ),
                rx.el.input(
                    type="number",
                    step="0.01",
                    on_change=IncidenciasState.set_pz_no_veta,
                    class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                    default_value=IncidenciasState.pz_no_veta.to_string(),
                ),
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4",
        ),
        rx.el.h4("Tapacantos", class_name="text-sm font-bold text-gray-800 mb-2 mt-4"),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Frontal",
                    class_name="block text-xs font-semibold text-gray-500 mb-1",
                ),
                rx.el.input(
                    on_change=IncidenciasState.set_pz_tc_f,
                    class_name="w-full px-3 py-2 border border-gray-200 rounded-xl text-sm",
                    default_value=IncidenciasState.pz_tc_f,
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Posterior",
                    class_name="block text-xs font-semibold text-gray-500 mb-1",
                ),
                rx.el.input(
                    on_change=IncidenciasState.set_pz_tc_p,
                    class_name="w-full px-3 py-2 border border-gray-200 rounded-xl text-sm",
                    default_value=IncidenciasState.pz_tc_p,
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Derecho",
                    class_name="block text-xs font-semibold text-gray-500 mb-1",
                ),
                rx.el.input(
                    on_change=IncidenciasState.set_pz_tc_d,
                    class_name="w-full px-3 py-2 border border-gray-200 rounded-xl text-sm",
                    default_value=IncidenciasState.pz_tc_d,
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Izquierdo",
                    class_name="block text-xs font-semibold text-gray-500 mb-1",
                ),
                rx.el.input(
                    on_change=IncidenciasState.set_pz_tc_i,
                    class_name="w-full px-3 py-2 border border-gray-200 rounded-xl text-sm",
                    default_value=IncidenciasState.pz_tc_i,
                ),
            ),
            class_name="grid grid-cols-4 gap-2 mb-6",
        ),
        rx.el.button(
            "➕ Añadir a Matriz",
            on_click=IncidenciasState.add_pieza_to_matrix,
            class_name="w-full sm:w-auto px-6 py-2 bg-gray-900 text-white font-bold rounded-xl hover:bg-black transition-colors",
        ),
    )


def material_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Descripción",
                    class_name="block text-sm font-semibold text-gray-700 mb-1",
                ),
                rx.el.input(
                    on_change=IncidenciasState.set_mat_descripcion,
                    class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                    default_value=IncidenciasState.mat_descripcion,
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Cantidad",
                    class_name="block text-sm font-semibold text-gray-700 mb-1",
                ),
                rx.el.input(
                    type="number",
                    on_change=IncidenciasState.set_mat_cantidad,
                    class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                    default_value=IncidenciasState.mat_cantidad.to_string(),
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Observaciones",
                    class_name="block text-sm font-semibold text-gray-700 mb-1",
                ),
                rx.el.input(
                    on_change=IncidenciasState.set_mat_observaciones,
                    class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                    default_value=IncidenciasState.mat_observaciones,
                ),
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6",
        ),
        rx.el.button(
            "➕ Añadir a Matriz",
            on_click=IncidenciasState.add_material_to_matrix,
            class_name="w-full sm:w-auto px-6 py-2 bg-gray-900 text-white font-bold rounded-xl hover:bg-black transition-colors",
        ),
    )


def row_pieza_tmp(pz: TmpPieza, idx: int) -> rx.Component:
    return rx.el.tr(
        rx.el.td(idx + 1, class_name="px-4 py-3 text-sm text-gray-500"),
        rx.el.td(
            pz["descripcion"], class_name="px-4 py-3 text-sm font-medium text-gray-900"
        ),
        rx.el.td(
            pz["cantidad"].to_string(), class_name="px-4 py-3 text-sm text-gray-600"
        ),
        rx.el.td(pz["ubicacion"], class_name="px-4 py-3 text-sm text-gray-600"),
        rx.el.td(pz["material"], class_name="px-4 py-3 text-sm text-gray-600"),
        rx.el.td(pz["veta"].to_string(), class_name="px-4 py-3 text-sm text-gray-600"),
        rx.el.td(
            pz["no_veta"].to_string(), class_name="px-4 py-3 text-sm text-gray-600"
        ),
        rx.el.td(
            f"F:{pz['tc_f']} P:{pz['tc_p']} D:{pz['tc_d']} I:{pz['tc_i']}",
            class_name="px-4 py-3 text-xs text-gray-500",
        ),
        rx.el.td(
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4"),
                on_click=lambda: IncidenciasState.remove_pieza(idx),
                class_name="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors",
            ),
            class_name="px-4 py-3",
        ),
        class_name="border-b border-gray-100 hover:bg-gray-50",
    )


def row_material_tmp(mat: TmpMaterial, idx: int) -> rx.Component:
    return rx.el.tr(
        rx.el.td(idx + 1, class_name="px-4 py-3 text-sm text-gray-500"),
        rx.el.td(
            mat["descripcion"], class_name="px-4 py-3 text-sm font-medium text-gray-900"
        ),
        rx.el.td(
            mat["cantidad"].to_string(), class_name="px-4 py-3 text-sm text-gray-600"
        ),
        rx.el.td(mat["observaciones"], class_name="px-4 py-3 text-sm text-gray-600"),
        rx.el.td(
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4"),
                on_click=lambda: IncidenciasState.remove_material(idx),
                class_name="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors",
            ),
            class_name="px-4 py-3",
        ),
        class_name="border-b border-gray-100 hover:bg-gray-50",
    )


def row_detalle_pieza(det: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(det["descripcion"], class_name="px-4 py-2 text-sm text-gray-800"),
        rx.el.td(det["cantidad"], class_name="px-4 py-2 text-sm text-gray-600"),
        rx.el.td(det["ubicacion"], class_name="px-4 py-2 text-sm text-gray-600"),
        rx.el.td(det["material"], class_name="px-4 py-2 text-sm text-gray-600"),
        rx.el.td(det["rotacion"], class_name="px-4 py-2 text-sm text-gray-600"),
        rx.el.td(det["veta"], class_name="px-4 py-2 text-sm text-gray-600"),
        rx.el.td(det["no_veta"], class_name="px-4 py-2 text-sm text-gray-600"),
        rx.el.td(det["tc_f"], class_name="px-4 py-2 text-sm text-gray-600"),
        rx.el.td(det["tc_p"], class_name="px-4 py-2 text-sm text-gray-600"),
        rx.el.td(det["tc_d"], class_name="px-4 py-2 text-sm text-gray-600"),
        rx.el.td(det["tc_i"], class_name="px-4 py-2 text-sm text-gray-600"),
        class_name="border-b border-gray-50 hover:bg-gray-50",
    )


def row_detalle_material(det: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(det["descripcion"], class_name="px-4 py-2 text-sm text-gray-800"),
        rx.el.td(det["cantidad"], class_name="px-4 py-2 text-sm text-gray-600"),
        rx.el.td(det["observaciones"], class_name="px-4 py-2 text-sm text-gray-600"),
        class_name="border-b border-gray-50 hover:bg-gray-50",
    )


def historial_item(inc: IncidenciaHistorialItem) -> rx.Component:
    is_expanded = IncidenciasState.expanded_ids.contains(inc["id"])
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    f"REQ-{inc['id']}",
                    class_name="px-2 py-1 bg-gray-100 text-gray-600 font-bold rounded text-xs",
                ),
                rx.el.span(inc["proyecto_label"], class_name="font-bold text-gray-900"),
                rx.el.span(
                    inc["tipo_requerimiento"], class_name="text-sm text-gray-500"
                ),
                rx.el.span(
                    inc["categoria"],
                    class_name="text-sm font-medium px-2 py-0.5 bg-blue-50 text-blue-700 rounded-full",
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.cond(inc["has_almacen"], "🟩", "🟥"),
                        rx.el.span(
                            "Alm", class_name="text-xs font-bold text-gray-500 ml-1"
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.div(
                        rx.cond(inc["has_solicitante"], "🟩", "🟥"),
                        rx.el.span(
                            "Sol", class_name="text-xs font-bold text-gray-500 ml-1"
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.div(
                        rx.cond(inc["has_teowin"], "🟩", "🟥"),
                        rx.el.span(
                            "Teo", class_name="text-xs font-bold text-gray-500 ml-1"
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex gap-3 mr-6",
                ),
                rx.el.span(inc["created_at"], class_name="text-sm text-gray-400 mr-4"),
                rx.icon(
                    rx.cond(is_expanded, "chevron-up", "chevron-down"),
                    class_name="h-5 w-5 text-gray-400",
                ),
                class_name="flex items-center",
            ),
            on_click=lambda: IncidenciasState.toggle_accordion(inc["id"]),
            class_name="flex justify-between items-center p-4 cursor-pointer hover:bg-gray-50 transition-colors",
        ),
        rx.cond(
            is_expanded,
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        inc["tipo_requerimiento"] == "Piezas",
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Descripción",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Ctd",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Ubicación",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Material",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Rot",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Veta",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "No Veta",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "TC F",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "TC P",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "TC D",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "TC I",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                )
                            ),
                            rx.el.tbody(rx.foreach(inc["detalles"], row_detalle_pieza)),
                            class_name="w-full table-auto border border-gray-100 rounded-lg overflow-hidden",
                        ),
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Descripción",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Ctd",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                    rx.el.th(
                                        "Observaciones",
                                        class_name="px-4 py-2 text-left text-xs text-gray-500 bg-gray-50",
                                    ),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(inc["detalles"], row_detalle_material)
                            ),
                            class_name="w-full table-auto border border-gray-100 rounded-lg overflow-hidden",
                        ),
                    ),
                    class_name="overflow-x-auto mb-6",
                ),
                rx.el.div(
                    rx.el.h4(
                        "Auditoría de Gestión",
                        class_name="text-sm font-bold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                rx.el.input(
                                    type="checkbox",
                                    checked=inc["has_almacen"],
                                    on_change=lambda _: IncidenciasState.toggle_fecha_field(
                                        inc["id"], "fecha_almacen"
                                    ),
                                    class_name="mr-2",
                                ),
                                "Almacén",
                                class_name="flex items-center font-semibold text-sm text-gray-700",
                            ),
                            rx.cond(
                                inc["has_almacen"],
                                rx.el.p(
                                    inc["fecha_almacen"],
                                    class_name="text-xs text-gray-500 mt-1 ml-5",
                                ),
                                rx.fragment(),
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                rx.el.input(
                                    type="checkbox",
                                    checked=inc["has_solicitante"],
                                    on_change=lambda _: IncidenciasState.toggle_fecha_field(
                                        inc["id"], "fecha_solicitante"
                                    ),
                                    class_name="mr-2",
                                ),
                                "Solicitante",
                                class_name="flex items-center font-semibold text-sm text-gray-700",
                            ),
                            rx.cond(
                                inc["has_solicitante"],
                                rx.el.p(
                                    inc["fecha_solicitante"],
                                    class_name="text-xs text-gray-500 mt-1 ml-5",
                                ),
                                rx.fragment(),
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                rx.el.input(
                                    type="checkbox",
                                    checked=inc["has_teowin"],
                                    on_change=lambda _: IncidenciasState.toggle_fecha_field(
                                        inc["id"], "fecha_teowin"
                                    ),
                                    class_name="mr-2",
                                ),
                                "Teowin",
                                class_name="flex items-center font-semibold text-sm text-gray-700",
                            ),
                            rx.cond(
                                inc["has_teowin"],
                                rx.el.p(
                                    inc["fecha_teowin"],
                                    class_name="text-xs text-gray-500 mt-1 ml-5",
                                ),
                                rx.fragment(),
                            ),
                        ),
                        class_name="flex flex-wrap gap-8 mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Observaciones de Gestión",
                            class_name="block text-sm font-semibold text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            default_value=inc["obs_gestion"],
                            on_blur=lambda val: IncidenciasState.update_obs_gestion(
                                inc["id"], val
                            ),
                            class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                        ),
                    ),
                    class_name="pt-4 border-t border-gray-100",
                ),
                class_name="p-4 bg-white border-t border-gray-100",
            ),
            rx.fragment(),
        ),
        class_name="bg-white border border-gray-200 rounded-xl mb-3 overflow-hidden shadow-sm",
    )


def tab_registro() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Seleccionar Proyecto",
                class_name="text-lg font-bold text-gray-800 mb-4",
            ),
            rx.el.div(
                rx.el.input(
                    placeholder="Buscar proyecto...",
                    on_change=IncidenciasState.set_search_project_text.debounce(300),
                    class_name="w-full md:w-1/3 px-4 py-2 border border-gray-200 rounded-xl",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("-- Seleccione un proyecto --", value=""),
                        rx.foreach(
                            IncidenciasState.filtered_projects,
                            lambda p: rx.el.option(p["label"], value=p["id"]),
                        ),
                        value=IncidenciasState.selected_project_id,
                        on_change=IncidenciasState.select_project_registro,
                        class_name="appearance-none w-full px-4 py-2 border border-gray-200 rounded-xl bg-white focus:ring-2 focus:ring-blue-500",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="absolute right-3 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                    ),
                    class_name="relative w-full md:w-2/3",
                ),
                class_name="flex flex-col md:flex-row gap-4",
            ),
            class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Tipo de Requerimiento",
                        class_name="block text-sm font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("Piezas", value="Piezas"),
                            rx.el.option("Materiales", value="Materiales"),
                            value=IncidenciasState.tipo_requerimiento,
                            on_change=IncidenciasState.set_tipo_requerimiento,
                            class_name="appearance-none w-full px-4 py-2 border border-gray-200 rounded-xl bg-white",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="absolute right-3 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                        ),
                        class_name="relative",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Categoría",
                        class_name="block text-sm font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("Faltante", value="Faltante"),
                            rx.el.option("Pieza Dañada", value="Pieza Dañada"),
                            rx.el.option("Cambio", value="Cambio"),
                            rx.el.option("Otro", value="Otro"),
                            value=IncidenciasState.categoria,
                            on_change=IncidenciasState.set_categoria,
                            class_name="appearance-none w-full px-4 py-2 border border-gray-200 rounded-xl bg-white",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="absolute right-3 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                        ),
                        class_name="relative",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
            ),
            class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm mb-6",
        ),
        rx.el.div(
            rx.el.h3(
                f"Formulario de {IncidenciasState.tipo_requerimiento}",
                class_name="text-lg font-bold text-gray-800 mb-4",
            ),
            rx.cond(IncidenciasState.show_piezas_form, pieza_form(), material_form()),
            class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm mb-6",
        ),
        rx.el.div(
            rx.el.h3(
                "Matriz Temporal", class_name="text-lg font-bold text-gray-800 mb-4"
            ),
            rx.el.div(
                rx.cond(
                    IncidenciasState.show_piezas_form,
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "#",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "Descripción",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "Ctd",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "Ubicación",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "Material",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "Veta",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "No Veta",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "TC(F/P/D/I)",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "Acciones",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                IncidenciasState.tmp_piezas,
                                lambda p, i: row_pieza_tmp(p, i),
                            )
                        ),
                        class_name="w-full table-auto",
                    ),
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "#",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "Descripción",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "Ctd",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "Observaciones",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "Acciones",
                                    class_name="px-4 py-2 text-left text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                IncidenciasState.tmp_materiales,
                                lambda m, i: row_material_tmp(m, i),
                            )
                        ),
                        class_name="w-full table-auto",
                    ),
                ),
                class_name="overflow-x-auto border border-gray-100 rounded-xl mb-6",
            ),
            rx.cond(
                IncidenciasState.reg_error != "",
                rx.el.p(
                    IncidenciasState.reg_error,
                    class_name="text-red-500 font-bold text-sm mb-4",
                ),
                rx.fragment(),
            ),
            rx.cond(
                IncidenciasState.reg_message != "",
                rx.el.p(
                    IncidenciasState.reg_message,
                    class_name="text-green-600 font-bold text-sm mb-4 bg-green-50 p-3 rounded-lg",
                ),
                rx.fragment(),
            ),
            rx.el.button(
                "🚀 Enviar Requerimiento",
                on_click=IncidenciasState.enviar_requerimiento,
                class_name="w-full py-3 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-colors shadow-sm text-lg",
            ),
            class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm",
        ),
        class_name="max-w-4xl mx-auto",
    )


def tab_historial() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Listado de Requerimientos",
            class_name="text-lg font-bold text-gray-800 mb-6",
        ),
        rx.el.div(rx.foreach(IncidenciasState.historial, historial_item)),
        class_name="max-w-5xl mx-auto",
    )


def incidencias_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.radix.tabs.root(
                rx.radix.tabs.list(
                    rx.radix.tabs.trigger(
                        rx.el.span(
                            "📝 Registro de Requerimiento",
                            class_name="flex items-center gap-2",
                        ),
                        value="registro",
                        class_name="px-4 py-2 font-semibold text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 outline-none",
                    ),
                    rx.radix.tabs.trigger(
                        rx.el.span(
                            "📋 Historial de Requerimientos",
                            class_name="flex items-center gap-2",
                        ),
                        value="historial",
                        class_name="px-4 py-2 font-semibold text-gray-600 hover:text-blue-600 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 outline-none",
                    ),
                    class_name="flex gap-4 border-b border-gray-200 mb-6",
                ),
                rx.radix.tabs.content(
                    tab_registro(), value="registro", class_name="outline-none"
                ),
                rx.radix.tabs.content(
                    tab_historial(), value="historial", class_name="outline-none"
                ),
                default_value="registro",
            ),
            class_name="max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700",
        ),
        "Incidencias y Requerimientos",
    )