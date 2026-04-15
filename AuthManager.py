import streamlit as st  # type: ignore


class AuthManager:
    def __init__(self, db_manager):
        self.db = db_manager

    def iniciar_sesion(self, email, password):
        try:
            # Autenticación segura usando el API nativo de Supabase Auth
            res = self.db.conn.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return res
        except Exception as e:
            st.error(f"Error de acceso: credenciales incorrectas o fallo de conexión. Detalle: {e}")
            return None

    def registrar_usuario(self, email, password):
        try:
            # Crea usuario en la tabla de auth genérica de Supabase
            res = self.db.conn.auth.sign_up({
                "email": email,
                "password": password
            })
            return res
        except Exception as e:
            st.error(f"Error al registrar usuario en Supabase Auth: {e}")
            return None

    def cerrar_sesion(self):
        self.db.conn.auth.sign_out()
        st.rerun()

    def verificar_sesion(self):
        # Retorna el usuario de la sesión JWT local si existe
        return self.db.conn.auth.get_user()