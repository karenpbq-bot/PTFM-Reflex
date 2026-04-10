import os
import pandas as pd
from supabase import create_client
from datetime import datetime
import logging


def fetch_all_paginated(query_builder, batch_size=1000):
    """Fetches all rows from a Supabase query, paginating in batches to avoid the 1000-row limit."""
    all_data = []
    offset = 0
    while True:
        res = query_builder.range(offset, offset + batch_size - 1).execute()
        all_data.extend(res.data)
        if len(res.data) < batch_size:
            break
        offset += batch_size
    return all_data


def conectar():
    url = os.environ.get("SUPABASE_URL", "https://afolglqvixpejyisgmin.supabase.co")
    key = os.environ.get(
        "SUPABASE_KEY",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFmb2xnbHF2aXhwZWp5aXNnbWluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0MzIyNjksImV4cCI6MjA4OTAwODI2OX0.0-tmQ0pwP4XPEDnG-3tDdRMrLz407n69jShxrmMWaaA",
    )
    return create_client(url, key)


def validar_usuario(usuario: str, clave: str):
    """
    Validates user credentials.
    Both username and password are strictly case-sensitive.
    """
    try:
        supabase = conectar()
        res = (
            supabase.table("usuarios")
            .select("*")
            .eq("nombre_usuario", usuario)
            .execute()
        )
        if res.data:
            for user_record in res.data:
                if user_record.get("contrasena") == clave:
                    return user_record
        return None
    except Exception as e:
        logging.exception(f"Error in validar_usuario: {e}")
        return None


def obtener_supervisores():
    try:
        supabase = conectar()
        if not supabase:
            return pd.DataFrame(columns=["id", "nombre_real", "rol"])
        res = (
            supabase.table("usuarios")
            .select("id, nombre_completo, rol")
            .in_("rol", ["admin", "Gerente", "Supervisor"])
            .execute()
        )
        df = pd.DataFrame(res.data)
        if not df.empty:
            df = df.rename(columns={"nombre_completo": "nombre_real"})
        return df
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Error al obtener supervisores: {e}")
        return pd.DataFrame(columns=["id", "nombre_real", "rol"])


def obtener_proyectos(palabra_clave=""):
    try:
        supabase = conectar()
        if not supabase:
            return pd.DataFrame()
        query = supabase.table("proyectos").select("*")
        if palabra_clave:
            query = query.or_(
                f"codigo.ilike.%{palabra_clave}%,proyecto_text.ilike.%{palabra_clave}%,cliente.ilike.%{palabra_clave}%"
            )
        res = query.execute()
        df = pd.DataFrame(res.data)
        if not df.empty:
            df["proyecto_display"] = (
                "[" + df["codigo"].astype(str) + "] " + df["proyecto_text"]
            )
        return df
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Error en obtener_proyectos: {e}")
        return pd.DataFrame()


def crear_proyecto(codigo, nombre, cliente, partida):
    try:
        supabase = conectar()
        if not supabase:
            return None
        data = {
            "codigo": codigo,
            "proyecto_text": nombre,
            "cliente": cliente,
            "partida": partida,
            "estatus": "Activo",
            "avance": 0,
        }
        return supabase.table("proyectos").insert(data).execute()
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Error al crear proyecto: {e}")
        return None


def eliminar_proyecto_completo(id_proyecto):
    try:
        supabase = conectar()
        if not supabase:
            return False
        res_prods = (
            supabase.table("productos")
            .select("id")
            .eq("proyecto_id", id_proyecto)
            .execute()
        )
        ids_productos = [p["id"] for p in res_prods.data]
        if ids_productos:
            supabase.table("seguimiento").delete().in_(
                "producto_id", ids_productos
            ).execute()
            supabase.table("productos_avance_valor").delete().in_(
                "producto_id", ids_productos
            ).execute()
        supabase.table("incidencias").delete().eq("proyecto_id", id_proyecto).execute()
        supabase.table("proyectos").delete().eq("id", id_proyecto).execute()
        return True
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Error al eliminar proyecto: {e}")
        return False


def obtener_productos_por_proyecto(id_proyecto):
    try:
        supabase = conectar()
        if not supabase:
            return pd.DataFrame()
        res = (
            supabase.table("productos")
            .select("*")
            .eq("proyecto_id", id_proyecto)
            .order("codigo_etiqueta")
            .execute()
        )
        return pd.DataFrame(res.data)
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Error en obtener_productos: {e}")
        return pd.DataFrame()


def obtener_seguimiento(id_producto):
    try:
        supabase = conectar()
        if not supabase:
            return pd.DataFrame()
        res = (
            supabase.table("seguimiento")
            .select("*")
            .eq("producto_id", id_producto)
            .execute()
        )
        return pd.DataFrame(res.data)
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Error en obtener_seguimiento: {e}")
        return pd.DataFrame()


def obtener_pesos_seguimiento():
    return {
        "Diseñado": 15,
        "Fabricado": 40,
        "Material en Obra": 5,
        "Material en Ubicación": 5,
        "Instalación de Estructura": 15,
        "Instalación de Puertas o Frentes": 10,
        "Revisión y Observaciones": 5,
        "Entrega": 5,
    }


def obtener_avance_por_hitos(id_proyecto, df_productos_filtrados=None):
    try:
        supabase = conectar()
        if not supabase:
            return {h: 0.0 for h in obtener_pesos_seguimiento().keys()}
        if df_productos_filtrados is None:
            res = (
                supabase.table("productos")
                .select("id")
                .eq("proyecto_id", id_proyecto)
                .execute()
            )
            df_p = pd.DataFrame(res.data)
        else:
            df_p = df_productos_filtrados
        HITOS_LIST = list(obtener_pesos_seguimiento().keys())
        if df_p.empty:
            return {h: 0.0 for h in HITOS_LIST}
        ids = df_p["id"].tolist()
        seg_data = fetch_all_paginated(
            supabase.table("seguimiento").select("hito").in_("producto_id", ids)
        )
        df_s = pd.DataFrame(seg_data)
        avances = {}
        total = len(df_p)
        if df_s.empty:
            return {h: 0.0 for h in HITOS_LIST}
        for h in HITOS_LIST:
            conteo = len(df_s[df_s["hito"] == h])
            avances[h] = round(conteo / total * 100, 1)
        return avances
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Error en obtener_avance_por_hitos: {e}")
        return {h: 0.0 for h in obtener_pesos_seguimiento().keys()}


def sincronizar_avances_estructural(codigo_p):
    try:
        supabase = conectar()
        if not supabase:
            return
        res_p = (
            supabase.table("proyectos")
            .select("id, proyecto_text, cliente")
            .eq("codigo", codigo_p)
            .single()
            .execute()
        )
        if not res_p.data:
            return
        p_id, p_nom, p_cli = (
            res_p.data["id"],
            res_p.data["proyecto_text"],
            res_p.data["cliente"],
        )
        res_prods = (
            supabase.table("productos").select("id").eq("proyecto_id", p_id).execute()
        )
        if not res_prods.data:
            return
        ids_prods = [p["id"] for p in res_prods.data]
        num_prods = len(ids_prods)
        seg_data = fetch_all_paginated(
            supabase.table("seguimiento")
            .select("producto_id, hito, fecha")
            .in_("producto_id", ids_prods)
        )
        df_seg = (
            pd.DataFrame(seg_data)
            if seg_data
            else pd.DataFrame(columns=["producto_id", "hito", "fecha"])
        )
        GRUPOS = {
            "av_diseno": ["Diseñado"],
            "av_fabricacion": ["Fabricado"],
            "av_traslado": ["Material en Obra", "Material en Ubicación"],
            "av_instalacion": [
                "Instalación de Estructura",
                "Instalación de Puertas o Frentes",
            ],
            "av_entrega": ["Revisión y Observaciones", "Entrega"],
        }
        fila = {
            "codigo": codigo_p,
            "proyecto_nombre": p_nom,
            "cliente": p_cli,
            "ultima_actualizacion": datetime.now().isoformat(),
        }
        fechas_reales = []
        if not df_seg.empty:
            df_seg["f_dt"] = pd.to_datetime(
                df_seg["fecha"], errors="coerce", dayfirst=True
            )
            fechas_reales = df_seg["f_dt"].dropna().tolist()
        for col, hitos in GRUPOS.items():
            conteo_etapa = len(df_seg[df_seg["hito"].isin(hitos)])
            max_posible = len(hitos) * num_prods
            fila[col] = (
                round(conteo_etapa / max_posible * 100, 1) if max_posible > 0 else 0
            )
        if fechas_reales:
            fila["fecha_inicio_real"] = min(fechas_reales).strftime("%Y-%m-%d")
            fila["fecha_fin_real"] = max(fechas_reales).strftime("%Y-%m-%d")
        supabase.table("avances_etapas").upsert(fila, on_conflict="codigo").execute()
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Falla en motor estructural: {e}")


def registrar_incidencia_detallada(
    proyecto_id, tipo, motivo, piezas, materiales, usuario_id
):
    try:
        supabase = conectar()
        if not supabase:
            return None
        detalle_final = piezas if tipo == "Piezas" else materiales
        data = {
            "proyecto_id": proyecto_id,
            "tipo_requerimiento": tipo,
            "categoria": motivo,
            "detalles": detalle_final,
            "supervisor_id": usuario_id,
            "estado": "Pendiente",
            "created_at": datetime.now().isoformat(),
        }
        return supabase.table("incidencias").insert(data).execute()
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Error en incidencia: {e}")
        return None


def obtener_incidencias_resumen():
    try:
        supabase = conectar()
        if not supabase:
            return pd.DataFrame()
        res = (
            supabase.table("incidencias")
            .select("*, proyectos(proyecto_text)")
            .order("created_at", desc=True)
            .execute()
        )
        if not res.data:
            return pd.DataFrame()
        for r in res.data:
            r["proyecto_text"] = (
                r["proyectos"].get("proyecto_text", "N/A")
                if r.get("proyectos")
                else "Sin Proyecto"
            )
        return pd.DataFrame(res.data)
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Error en historial incidencias: {e}")
        return pd.DataFrame()


def actualizar_gestion_incidencia(inc_id, datos_dict):
    try:
        supabase = conectar()
        if not supabase:
            return None
        datos_limpios = {k: str(v) if v else "" for k, v in datos_dict.items()}
        return (
            supabase.table("incidencias")
            .update(datos_limpios)
            .eq("id", inc_id)
            .execute()
        )
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Error en base de datos: {e}")
        return None


def eliminar_usuario_bd(id_usuario):
    try:
        supabase = conectar()
        if not supabase:
            return None
        return supabase.table("usuarios").delete().eq("id", id_usuario).execute()
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Error al eliminar usuario: {e}")
        return None


def actualizar_usuario_bd(id_usuario, datos):
    try:
        supabase = conectar()
        if not supabase:
            return None
        return supabase.table("usuarios").update(datos).eq("id", id_usuario).execute()
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Error al actualizar usuario: {e}")
        return None