import os

import streamlit as st
from st_supabase_connection import SupabaseConnection

try:
    from streamlit.errors import StreamlitSecretNotFoundError
except ImportError:
    StreamlitSecretNotFoundError = KeyError


def _credenciales_supabase():
    """Lee SUPABASE_* del entorno primero (Codespaces); si falta algo, usa secrets.toml."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if url:
        url = str(url).strip()
    if key:
        key = str(key).strip()
    if url and key:
        return url, key
    try:
        sec = st.secrets["connections"]["supabase"]
        if isinstance(sec, dict):
            if not url:
                url = sec.get("SUPABASE_URL") or sec.get("url")
            if not key:
                key = sec.get("SUPABASE_KEY") or sec.get("key")
    except (StreamlitSecretNotFoundError, KeyError, TypeError):
        pass
    if url:
        url = str(url).strip()
    if key:
        key = str(key).strip()
    return url, key


def get_supabase_connection():
    """Conexión única con credenciales explícitas."""
    url, key = _credenciales_supabase()
    if not url or not key:
        raise ValueError(
            "Faltan SUPABASE_URL y SUPABASE_KEY. Opciones: "
            "(1) Archivo .streamlit/secrets.toml con [connections.supabase]; "
            "(2) En Codespaces: Settings → Secrets and variables → Codespaces → "
            "añadir secretos de repositorio SUPABASE_URL y SUPABASE_KEY; "
            "(3) export SUPABASE_URL=... y SUPABASE_KEY=... en la terminal antes de arrancar."
        )
    try:
        return st.connection(
            "supabase",
            type=SupabaseConnection,
            url=url,
            key=key,
        )
    except TypeError:
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
