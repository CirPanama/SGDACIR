# ⚖️ SGDACIR - Sistema de Gestión Legal en Panamá

**SGDACIR** es un completo sistema web diseñado para la administración ágil de despachos de abogados y notarías en Panamá, priorizando la ciberseguridad, inmutabilidad de la auditoría y cumplimiento estricto con los principios de protección descritos en la **Ley 81 de Protección de Datos Personales**.

---

## 🔒 Arquitectura y Seguridad
Construido bajo un robusto modelo Serverless **(Frontend: Streamlit | BaaS: Supabase)**.  

Sus pilares fundamentales de seguridad consisten en:
1. **Autenticación Fuerte:** Gestión criptográfica y emisión de tokens (JWT) mediante la infraestructura global de *Supabase Auth*. Las contraseñas están fuertemente protegidas.
2. **Acceso a Datos Restringido (RLS):** Total privacidad sobre los expedientes y clientes usando *Row Level Security* directamente en el dialecto PostgreSQL.
3. **Auditoría Inalterable:** Triggers y métodos almacenados que bloquean la creación fraudulenta de logs, capturando todo movimiento de la base de datos de manera automatizada.

---

## 🚀 Despliegue en GitHub Codespaces (Recomendado)

Este proyecto viene preconfigurado con una carpeta noble (`.devcontainer`) que automatiza totalmente su despliegue y construcción en entornos de Microsoft/Github.

**¿Cómo arrancar tu entorno de desarrollo en 3 clics?**
1. Ve a la página principal de este repositorio en GitHub.
2. Haz clic en el botón verde `<> Code`.
3. Dirígete a la pestaña **Codespaces** y haz clic en **Create codespace on main**.
4. ¡Espera un par de minutos! GitHub Codespaces configurará Ubuntu, instalará la versión correcta de Python y ejecutará las dependencias de `requirements.txt` por ti.

---

## 💻 Ejecución Local / Standalone

Si deseas levantar el servidor localmente en tu computadora personal, sigue estos pasos:

### 1. Variables de Entorno y Secretos
Crea e inyecta tus credenciales del panel de API de Supabase en un archivo llamado **`.env`** en la carpeta principal raíz:

```env
SUPABASE_URL="https://tu-proyecto.supabase.co"
SUPABASE_KEY="tu-anon-key-publica"
```

### 2. Instalar el Ecosistema Python
Asegúrate de contar con Python 3 instalado en tu sistema y ejecuta:

```bash
python -m pip install -r requirements.txt
```

### 3. ¡Despegue del Servidor!
Teniendo los requerimientos listos, utiliza nuestro atajo cruzado para iniciar la plataforma en un puerto local (generalmente el `8501`).

```bash
python -m streamlit run app.py
```

---

## 🛠 Instalación Base de Datos (Primer uso)
Si estás clonando este proyecto tú mismo en una cuenta de **Supabase** vacía:

1. Ingresa al panel `SQL Editor` en tu Dashboard de Supabase.
2. Carga y ejecuta por completo el archivo `scripts_seguridad_bd.sql`. 
3. *Aviso importante:* Esto bloqueará todas tus tablas de fraude e inyectará los candados de seguridad necesarios para las reglas RLS de tu nuevo despacho virtual.
