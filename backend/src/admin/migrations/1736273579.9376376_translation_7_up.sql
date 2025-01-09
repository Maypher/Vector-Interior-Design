ALTER TABLE IF EXISTS administration.usuario RENAME TO admin_user;

ALTER SEQUENCE obra_indice_seq RENAME TO project_index_seq;
ALTER TABLE IF EXISTS obra RENAME TO project;
ALTER TABLE IF EXISTS project RENAME COLUMN nombre TO "name";
ALTER TABLE IF EXISTS project RENAME COLUMN descripcion TO description;
ALTER TABLE IF EXISTS project RENAME COLUMN indice TO "index";
ALTER TABLE IF EXISTS project ALTER COLUMN "index" SET DEFAULT nextval('project_index_seq')::FLOAT;
ALTER TABLE IF EXISTS project RENAME COLUMN publico TO public;
ALTER TABLE IF EXISTS project RENAME COLUMN imagen_principal TO main_image;

ALTER SEQUENCE ambiente_indice_seq RENAME TO space_index_seq;
ALTER TABLE IF EXISTS ambiente RENAME TO space;
ALTER TABLE IF EXISTS space RENAME COLUMN nombre TO "name";
ALTER TABLE IF EXISTS space RENAME COLUMN descripcion TO description;
ALTER TABLE IF EXISTS space RENAME COLUMN obra_id TO project_id;
ALTER TABLE IF EXISTS space RENAME COLUMN indice TO "index";
ALTER TABLE IF EXISTS space ALTER COLUMN "index" SET DEFAULT nextval('space_index_seq')::FLOAT;

ALTER SEQUENCE imagen_indice_seq RENAME TO image_index_seq;
ALTER TABLE IF EXISTS imagen RENAME TO image;
ALTER TABLE IF EXISTS image RENAME COLUMN archivo TO filename;
ALTER TABLE IF EXISTS image RENAME COLUMN texto_alt TO alt_text;
ALTER TABLE IF EXISTS image RENAME COLUMN indice TO "index";
ALTER TABLE IF EXISTS image ALTER COLUMN "index" SET DEFAULT nextval('image_index_seq')::FLOAT;
ALTER TABLE IF EXISTS image RENAME COLUMN ambiente_id TO space_id;
ALTER TABLE IF EXISTS image RENAME COLUMN pagina_principal TO main_page;
ALTER TABLE IF EXISTS image RENAME COLUMN tlfnconfig TO phone_config;
ALTER TABLE IF EXISTS image RENAME COLUMN descripcion TO description;
ALTER TABLE IF EXISTS image RENAME COLUMN descripciontipografia TO description_font;
ALTER TABLE IF EXISTS image RENAME COLUMN esconderenobra TO hide_in_project;

ALTER SEQUENCE pag_principal_indice_seq RENAME TO main_page_index_seq;
ALTER TABLE IF EXISTS imagenconfig RENAME TO main_page_config;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN imagen_id TO image_id;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN imagen_borde_n TO image_border_n;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN imagen_borde_s TO image_border_s;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN imagen_borde_e TO image_border_e;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN imagen_borde_o TO image_border_w;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN descripcion TO description_es;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN descripcion_en TO description_en;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN texto_ubicacion TO description_position;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN descripciontipografia TO description_font;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN descripciontamano TO description_font_size;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN descripciondistribucion TO description_alignment;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN logo_ubicacion TO logo_position;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN logo_borde_n TO logo_border_n;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN logo_borde_s TO logo_border_s;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN logo_borde_e TO logo_border_e;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN logo_borde_o TO logo_border_w;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN sangrar TO overflow;
ALTER TABLE IF EXISTS main_page_config RENAME COLUMN indice TO "index";
ALTER TABLE IF EXISTS main_page_config ALTER COLUMN "index" SET DEFAULT nextval('main_page_index_seq')::FLOAT;

ALTER TYPE alineacionimagen RENAME TO image_alignment;
ALTER TYPE image_alignment RENAME VALUE 'IZQUIERDA' TO 'LEFT';
ALTER TYPE image_alignment RENAME VALUE 'DERECHA' TO 'RIGHT';
ALTER TYPE image_alignment RENAME VALUE 'CENTRO' TO 'CENTER';
ALTER TYPE image_alignment RENAME VALUE 'SANGRAR' TO 'OVERFLOW';

ALTER TYPE ubicacion RENAME TO location;
ALTER TYPE location RENAME VALUE 'O' TO 'W';

ALTER TYPE imagentlfnconfig RENAME TO image_phone_config;
ALTER TYPE image_phone_config RENAME ATTRIBUTE bordes TO borders CASCADE;
ALTER TYPE image_phone_config RENAME ATTRIBUTE alineacion TO alignment CASCADE;
ALTER TYPE image_phone_config RENAME ATTRIBUTE descripcionubicacion TO description_position CASCADE;
ALTER TYPE image_phone_config RENAME ATTRIBUTE descripcionalineacion TO description_alignment CASCADE;

ALTER FUNCTION validate_imagen_principal() RENAME TO validate_main_image;
CREATE OR REPLACE FUNCTION validate_main_image()
RETURNS TRIGGER AS $$
BEGIN
    -- If imagen_principal is not null, check its validity
    IF NEW.main_image IS NOT NULL THEN
        -- Check if the image exists and belongs to an ambiente of the same obra
        IF NOT EXISTS (
            SELECT
            FROM public.image img
            JOIN public.space spc ON img.space_id = spc.id
            WHERE img.id = NEW.main_image
              AND spc.project_id = NEW.id
        ) THEN
            RAISE EXCEPTION 'Main image must belong to an space of the same project' USING ERRCODE = 'P0001';
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS check_imagen_principal_trigger ON project;
CREATE TRIGGER check_main_image_trigger
BEFORE INSERT OR UPDATE ON public.project
FOR EACH ROW
EXECUTE FUNCTION validate_main_image();
