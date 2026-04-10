import reflex as rx
from app.components.navigation import layout
from app.pages.seguimiento import seguimiento_page
from app.pages.proyectos import proyectos_page
from app.pages.metricas import metricas_page
from app.pages.incidencias import incidencias_page


def index() -> rx.Component:
    return seguimiento_page()


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    ],
    head_components=[
        rx.el.script(src="https://cdn.plot.ly/plotly-3.4.0.min.js"),
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
from app.states.seguimiento_state import SeguimientoState
from app.states.proyectos_state import ProyectosState
from app.states.metricas_state import MetricasState
from app.states.incidencias_state import IncidenciasState
from app.states.usuarios_state import UsuariosState
from app.pages.login import login_page
from app.pages.usuarios import usuarios_page

app.add_page(index, route="/", on_load=[SeguimientoState.load_projects_list])
app.add_page(login_page, route="/login")
app.add_page(
    proyectos_page,
    route="/proyectos",
    on_load=[ProyectosState.load_projects, ProyectosState.load_projects_with_details],
)
app.add_page(
    seguimiento_page,
    route="/seguimiento",
    on_load=[SeguimientoState.load_projects_list],
)
app.add_page(metricas_page, route="/metricas", on_load=[MetricasState.load_metricas])
app.add_page(
    incidencias_page, route="/incidencias", on_load=[IncidenciasState.load_incidencias]
)
app.add_page(usuarios_page, route="/usuarios", on_load=[UsuariosState.load_users])