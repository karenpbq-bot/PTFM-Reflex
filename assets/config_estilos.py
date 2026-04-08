AZUL_CLARO_MENU = "#E6F2FF"
TEXTO_MENU = "#002147"
NARANJA_ACENTO = "#FF8C00"
BLANCO_FONDO = "#F5F5F5"
TEXTO_GENERAL = "#333333"
TITULO_APP = "Gestión de Carpintería Industrial"
ICONO_FAVICON = "📐"
ESTILOS_CSS = f'\n<style>\n    /* Estilo para los botones principales (Naranja) */\n    .stButton>button {{\n        background-color: {NARANJA_ACENTO};\n        color: white;\n        border-radius: 8px;\n        border: none;\n        font-weight: bold;\n    }}\n    \n    /* Configuración del Menú Lateral (Fondo claro) */\n    [data-testid="stSidebar"] {{\n        background-color: {AZUL_CLARO_MENU};\n    }}\n    \n    /* Forzar que todos los textos del menú sean oscuros */\n    [data-testid="stSidebar"] * {{\n        color: {TEXTO_MENU} !important;\n    }}\n\n    /* Estilo opcional: Títulos del cuerpo en azul oscuro */\n    h1, h2, h3 {{\n        color: {TEXTO_MENU};\n    }}\n</style>\n'