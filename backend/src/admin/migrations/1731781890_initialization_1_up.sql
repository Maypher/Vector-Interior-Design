CREATE TABLE administration.usuario (
    id SMALLSERIAL PRIMARY KEY,
    name VARCHAR(75) NOT NULL,
    email VARCHAR(75) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL
);

CREATE TABLE administration.session (
    id SMALLSERIAL PRIMARY KEY,
    session_id VARCHAR(200) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    user_id INTEGER REFERENCES administration.usuario ON DELETE CASCADE
);

CREATE TABLE public.obra (
    id SMALLSERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    publico BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE public.ambiente (
    id SMALLSERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    obra_id INTEGER REFERENCES obra ON DELETE CASCADE,
    indice INT NOT NULL,
    CONSTRAINT repeated_index_ambiente UNIQUE (obra_id, indice) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT repeated_name UNIQUE (obra_id, nombre)
);

CREATE TABLE public.imagen (
    id SMALLSERIAL PRIMARY KEY,
    archivo VARCHAR(255) UNIQUE NOT NULL,
    texto_alt VARCHAR(255) NOT NULL,
    indice INT NOT NULL,
    ambiente_id INTEGER REFERENCES ambiente ON DELETE CASCADE,
    CONSTRAINT repeated_index_image UNIQUE (ambiente_id, indice) DEFERRABLE INITIALLY DEFERRED
);
-- Done this way because of circular dependencies
ALTER TABLE public.obra ADD COLUMN imagen_principal INTEGER REFERENCES imagen;

CREATE OR REPLACE FUNCTION adjust_list_order()
RETURNS TRIGGER AS $$
DECLARE
    old_index INT;
    new_index INT;
    max_index INT;

    target_column text := TG_ARGV[0];
BEGIN
    -- Get the old and new indices
    old_index := OLD.indice;
    new_index := NEW.indice;

    EXECUTE format(
        'SELECT COALESCE(MAX(indice), 0) FROM %I
        WHERE %I = $1.%s;', 
        TG_TABLE_NAME, target_column, target_column
    ) USING NEW INTO max_index;

    -- Clamp the new index to the range [0, max_index]
    new_index := LEAST(GREATEST(new_index, 0), max_index);

    -- If the order_index is not changing, do nothing
    IF old_index IS NOT DISTINCT FROM new_index THEN
        NEW.indice := new_index;
        RETURN NEW;
    END IF;

    -- Handle moving to a lower index (e.g., 2 -> 0)
    IF new_index < old_index THEN
       EXECUTE format (
            'UPDATE %I
            SET indice = indice + 1
            WHERE %I = $1.%s
            AND indice >= %s
            AND indice < %s;',
            TG_TABLE_NAME, target_column, target_column, new_index, old_index
        ) USING NEW;

    -- Handle moving to a higher index (e.g., 0 -> 2)
    ELSIF new_index > old_index THEN
        EXECUTE format (
            'UPDATE %I
            SET indice = indice - 1
            WHERE %I = $1.%s
            AND indice > %s
            AND indice <= %s;',
            TG_TABLE_NAME, target_column, target_column, old_index, new_index
        ) USING NEW;
    END IF;

    -- Update the moved image to its final index
    NEW.indice := new_index;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER adjust_image_order
BEFORE UPDATE OF indice ON imagen
FOR EACH ROW
WHEN (pg_trigger_depth() < 1)
EXECUTE FUNCTION adjust_list_order("ambiente_id");

CREATE TRIGGER adjust_ambiente_order
BEFORE UPDATE OF indice ON ambiente
FOR EACH ROW
WHEN (pg_trigger_depth() < 1)
EXECUTE FUNCTION adjust_list_order("obra_id");

CREATE OR REPLACE FUNCTION assign_indice()
RETURNS TRIGGER AS $$
DECLARE
    target_column text := TG_ARGV[0];
    new_index int;
BEGIN

    EXECUTE format(
        'SELECT COALESCE(
        (SELECT MAX(indice) FROM %I WHERE %I = $1.%s), 
        -1
        ) + 1;',
        TG_TABLE_NAME, target_column, target_column
    ) USING NEW INTO new_index;

    NEW.indice := new_index;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_assign_indice_image
BEFORE INSERT ON imagen
FOR EACH ROW
EXECUTE FUNCTION assign_indice("ambiente_id");

CREATE TRIGGER trigger_assign_indice_ambiente
BEFORE INSERT ON ambiente
FOR EACH ROW
EXECUTE FUNCTION assign_indice("obra_id");

-- Create a function to validate the imagen_principal constraint
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

-- Create a trigger to enforce the constraint
CREATE TRIGGER check_imagen_principal_trigger
BEFORE INSERT OR UPDATE ON public.obra
FOR EACH ROW
EXECUTE FUNCTION validate_imagen_principal();
