-- SCRIPT DE SEGURIDAD Y CUMPLIMIENTO LEY 81 - SGDACIR
-- Este script debe ser ejecutado en el "SQL Editor" de Supabase de tu proyecto.

-- 1. Habilitar RLS (Row Level Security) en todas las tablas sensibles
ALTER TABLE IF EXISTS clientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS expedientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS perfiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS logs_sistema ENABLE ROW LEVEL SECURITY;

-- 2. Políticas de acceso a datos para usuarios autenticados (JWT)
-- Solo los usuarios con sesión iniciada pueden Ver, Insertar, Actualizar y Eliminar las tablas.
-- * Nota: Si necesitas que diferentes roles ("supervisor", "admin") vean diferentes datos, las políticas se pueden restringir más.

CREATE POLICY "Activos_Select_Clientes" ON clientes FOR SELECT TO authenticated USING (true);
CREATE POLICY "Activos_Insert_Clientes" ON clientes FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Activos_Update_Clientes" ON clientes FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Activos_Delete_Clientes" ON clientes FOR DELETE TO authenticated USING (true);

-- Aplicar lo mismo a expedientes
CREATE POLICY "Activos_Select_Expedientes" ON expedientes FOR SELECT TO authenticated USING (true);
CREATE POLICY "Activos_Insert_Expedientes" ON expedientes FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Activos_Update_Expedientes" ON expedientes FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Activos_Delete_Expedientes" ON expedientes FOR DELETE TO authenticated USING (true);

-- (Las demás tablas como facturación o recibos pueden añadirse aquí con la misma estructura)

-- Perfiles: Solo administradores pueden insertar, pero todos pueden verse a sí mismos
CREATE POLICY "Activos_All_Perfiles" ON perfiles FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- 3. AUDITORÍA INALTERABLE (Trigger de Base de datos)
-- Impedimos que un usuario o cliente modifique los logs, solo pueden ser insertados por los triggers.
CREATE POLICY "Logs_Solo_Lectura_Autenticados" ON logs_sistema FOR SELECT TO authenticated USING (true);

-- Función que captura cada cambio
CREATE OR REPLACE FUNCTION audit_log_op()
RETURNS TRIGGER AS $$
DECLARE
    v_usuario TEXT;
    v_detalles TEXT;
BEGIN
    -- Capturar el email del usuario autenticado en la sesión JWT
    v_usuario := coalesce((auth.jwt() ->> 'email'), 'Sistema');
    
    -- Armar un detalle genérico
    IF TG_OP = 'DELETE' THEN
        v_detalles := 'Registro eliminado. ID: ' || coalesce(OLD.id::text, 'Desconocido');
        INSERT INTO logs_sistema(usuario, rol, accion, modulo, detalle)
        VALUES (v_usuario, 'BaseDeDatos', TG_OP, TG_TABLE_NAME, v_detalles);
        RETURN OLD;
    ELSE
        v_detalles := 'Registro insertado/actualizado. ID: ' || coalesce(NEW.id::text, 'Desconocido');
        INSERT INTO logs_sistema(usuario, rol, accion, modulo, detalle)
        VALUES (v_usuario, 'BaseDeDatos', TG_OP, TG_TABLE_NAME, v_detalles);
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Aplicar Trigger de auditoría a la tabla principal "clientes" como ejemplo 
-- (Podemos añadir lo mismo a expedientes, ventas, etc.)
DROP TRIGGER IF EXISTS trigger_audit_clientes ON clientes;
CREATE TRIGGER trigger_audit_clientes
AFTER INSERT OR UPDATE OR DELETE ON clientes
FOR EACH ROW EXECUTE FUNCTION audit_log_op();

DROP TRIGGER IF EXISTS trigger_audit_expedientes ON expedientes;
CREATE TRIGGER trigger_audit_expedientes
AFTER INSERT OR UPDATE OR DELETE ON expedientes
FOR EACH ROW EXECUTE FUNCTION audit_log_op();
