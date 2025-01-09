ALTER TABLE IF EXISTS administration.admin_user RENAME TO usuario;

ALTER SEQUENCE project_index_seq RENAME TO obra_indice_seq;
ALTER TABLE IF EXISTS project RENAME TO obra;
ALTER TABLE IF EXISTS obra RENAME COLUMN "name" TO nombre;
ALTER TABLE IF EXISTS obra RENAME COLUMN description TO descripcion;
ALTER TABLE IF EXISTS obra RENAME COLUMN "index" TO indice;
ALTER TABLE IF EXISTS obra ALTER COLUMN indice SET DEFAULT nextval('obra_indice_seq')::FLOAT;
ALTER TABLE IF EXISTS obra RENAME COLUMN public TO publico;
ALTER TABLE IF EXISTS obra RENAME COLUMN main_image TO imagen_principal;

ALTER SEQUENCE space_index_seq RENAME TO ambiente_indice_seq;
ALTER TABLE IF EXISTS space RENAME TO ambiente;
ALTER TABLE IF EXISTS ambiente RENAME COLUMN "name" TO nombre;
ALTER TABLE IF EXISTS ambiente RENAME COLUMN description TO descripcion;
ALTER TABLE IF EXISTS ambiente RENAME COLUMN project_id TO obra_id;
ALTER TABLE IF EXISTS ambiente RENAME COLUMN "index" TO indice;
ALTER TABLE IF EXISTS ambiente ALTER COLUMN indice SET DEFAULT nextval('ambiente_indice_seq')::FLOAT;

ALTER SEQUENCE image_index_seq RENAME TO imagen_indice_seq;
ALTER TABLE IF EXISTS image RENAME TO imagen;
ALTER TABLE IF EXISTS imagen RENAME COLUMN filename TO archivo;
ALTER TABLE IF EXISTS imagen RENAME COLUMN alt_text TO texto_alt;
ALTER TABLE IF EXISTS imagen RENAME COLUMN "index" TO indice;
ALTER TABLE IF EXISTS imagen ALTER COLUMN indice SET DEFAULT nextval('imagen_indice_seq')::FLOAT;
ALTER TABLE IF EXISTS imagen RENAME COLUMN space_id TO ambiente_id;
ALTER TABLE IF EXISTS imagen RENAME COLUMN main_page TO pagina_principal;
ALTER TABLE IF EXISTS imagen RENAME COLUMN phone_config TO tlfnconfig;
ALTER TABLE IF EXISTS imagen RENAME COLUMN description TO descripcion;
ALTER TABLE IF EXISTS imagen RENAME COLUMN description_font TO descripciontipografia;
ALTER TABLE IF EXISTS imagen RENAME COLUMN hide_in_project TO esconderenobra;

ALTER SEQUENCE main_page_index_seq RENAME TO pag_principal_indice_seq;
ALTER TABLE IF EXISTS main_page_config RENAME TO imagenconfig;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN image_id TO imagen_id;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN image_border_n TO imagen_borde_n;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN image_border_s TO imagen_borde_s;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN image_border_e TO imagen_borde_e;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN image_border_w TO imagen_borde_o;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN description_es TO descripcion;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN description_en TO descripcion_en;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN description_position TO texto_ubicacion;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN description_font TO descripciontipografia;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN description_font_size TO descripciontamano;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN description_alignment TO descripciondistribucion;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN logo_position TO logo_ubicacion;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN logo_border_n TO logo_borde_n;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN logo_border_s TO logo_borde_s;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN logo_border_e TO logo_borde_e;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN logo_border_w TO logo_borde_o;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN overflow TO sangrar;
ALTER TABLE IF EXISTS imagenconfig RENAME COLUMN "index" TO indice;
ALTER TABLE IF EXISTS main_page_config ALTER COLUMN indice SET DEFAULT nextval('pag_principal_indice_seq')::FLOAT;

ALTER TYPE image_alignment RENAME TO alineacionimagen;
ALTER TYPE alineacionimagen RENAME VALUE 'LEFT' TO 'IZQUIERDA';
ALTER TYPE alineacionimagen RENAME VALUE 'RIGHT' TO 'DERECHA';
ALTER TYPE alineacionimagen RENAME VALUE 'CENTER' TO 'CENTRO';
ALTER TYPE alineacionimagen RENAME VALUE 'OVERFLOW' TO 'SANGRAR';

ALTER TYPE location RENAME TO ubicacion;
ALTER TYPE ubicacion RENAME VALUE 'W' TO 'O';

ALTER TYPE image_phone_config RENAME TO imagentlfnconfig;
ALTER TYPE imagentlfnconfig RENAME ATTRIBUTE borders TO bordes CASCADE;
ALTER TYPE imagentlfnconfig RENAME ATTRIBUTE alignment TO alineacion CASCADE;
ALTER TYPE imagentlfnconfig RENAME ATTRIBUTE description_position TO descripcionubicacion CASCADE;
ALTER TYPE imagentlfnconfig RENAME ATTRIBUTE description_alignment TO descripcionalineacion CASCADE;

ALTER FUNCTION validate_main_image() RENAME TO validate_imagen_principal;
CREATE OR REPLACE FUNCTION validate_imagen_principal()
RETURNS TRIGGER AS $$
BEGIN
    -- If imagen_principal is not null, check its validity
    IF NEW.imagen_principal IS NOT NULL THEN
        -- Check if the image exists and belongs to an ambiente of the same obra
        IF NOT EXISTS (
            SELECT
            FROM public.imagen img
            JOIN public.ambiente amb ON img.ambiente_id = amb.id
            WHERE img.id = NEW.imagen_principal
              AND amb.obra_id = NEW.id
        ) THEN
            RAISE EXCEPTION 'Imagen principal must belong to an ambiente of the same obra' USING ERRCODE = 'P0001';
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS check_main_image_trigger ON obra;
CREATE TRIGGER check_imagen_principal_trigger
BEFORE INSERT OR UPDATE ON public.obra
FOR EACH ROW
EXECUTE FUNCTION validate_imagen_principal();
