import streamlit as st
from st_supabase_connection import SupabaseConnection


def _credenciales_supabase():
    """Lee URL y clave con el formato oficial (SUPABASE_*) o el alternativo (url/key)."""
    try:
        sec = st.secrets["connections"]["supabase"]
    except (KeyError, TypeError):
        return None, None
    url = sec.get("SUPABASE_URL") or sec.get("url")
    key = sec.get("SUPABASE_KEY") or sec.get("key")
    if url:
        url = str(url).strip()
    if key:
        key = str(key).strip()
    return url, key


def get_supabase_connection():
    """Conexión única con credenciales explícitas para evitar fallos por nombres de clave."""
    url, key = _credenciales_supabase()
    if not url or not key:
        raise ValueError(
            "Faltan credenciales en .streamlit/secrets.toml: "
            "defina SUPABASE_URL y SUPABASE_KEY bajo [connections.supabase]."
        )
    try:
        return st.connection(
            "supabase",
            type=SupabaseConnection,
            url=url,
            key=key,
        )
    except TypeError:
        # Compatibilidad si la versión de Streamlit no acepta url/key como kwargs
        return st.connection("supabase", type=SupabaseConnection)


class LegalDB:
    def __init__(self):
        self.conn = get_supabase_connection()

    def table(self, tabla):
        return self.conn.table(tabla)

    def fetch(self, tabla):
        """Obtiene datos para Contabilidad y Configuración"""
        try:
            res = self.conn.table(tabla).select("*").execute()
            return res.data if res.data else []
        except Exception as e:
            st.error(f"Error en DB ({tabla}): {e}")
            return []

    def insert(self, tabla, datos):
        """Inserción con manejo de errores de red/API"""
        try:
            return self.conn.table(tabla).insert(datos).execute()
        except Exception as e:
            st.error(f"No se pudo insertar en {tabla}: {e}")
            return None

    def update(self, tabla, datos, id_registro):
        """Actualización para el módulo de Configuración"""
        try:
            return self.conn.table(tabla).update(datos).eq("id", id_registro).execute()
        except Exception as e:
            st.error(f"No se pudo actualizar {tabla} (id={id_registro}): {e}")
            return None
