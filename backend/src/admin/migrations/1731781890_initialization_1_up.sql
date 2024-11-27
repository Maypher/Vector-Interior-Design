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
    descripcion TEXT NOT NULL
);

CREATE TABLE public.imagen (
    id SMALLSERIAL PRIMARY KEY,
    archivo VARCHAR(255) UNIQUE NOT NULL,
    texto_alt VARCHAR(255) NOT NULL,
    indice INT NOT NULL,
    obra_id INTEGER REFERENCES obra ON DELETE CASCADE,
    UNIQUE (obra_id, indice) DEFERRABLE INITIALLY DEFERRED
);

CREATE OR REPLACE FUNCTION adjust_image_order()
RETURNS TRIGGER AS $$
DECLARE
    old_index INT;
    new_index INT;
    max_index INT;
BEGIN
    -- Get the old and new indices
    old_index := OLD.indice;
    new_index := NEW.indice;

    SELECT COALESCE(MAX(indice), 0) INTO max_index
    FROM imagen
    WHERE obra_id = NEW.obra_id;

    -- Clamp the new index to the range [0, max_index]
    new_index := LEAST(GREATEST(new_index, 0), max_index);

    -- If the order_index is not changing, do nothing
    IF old_index IS NOT DISTINCT FROM new_index THEN
        RETURN NEW;
    END IF;

    -- Handle moving to a lower index (e.g., 2 -> 0)
    IF new_index < old_index THEN
        UPDATE imagen
        SET indice = indice + 1
        WHERE obra_id = NEW.obra_id
        AND indice >= new_index
        AND indice < old_index;

    -- Handle moving to a higher index (e.g., 0 -> 2)
    ELSIF new_index > old_index THEN
        UPDATE imagen
        SET indice = indice - 1
        WHERE obra_id = NEW.obra_id
        AND indice > old_index
        AND indice <= new_index;
    END IF;

    -- Update the moved image to its final index
    NEW.indice := new_index;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER adjust_image_order_trigger
BEFORE UPDATE OF indice ON imagen
FOR EACH ROW
WHEN (pg_trigger_depth() = 0)
EXECUTE FUNCTION adjust_image_order();

CREATE OR REPLACE FUNCTION assign_indice()
RETURNS TRIGGER AS $$
BEGIN
    NEW.indice := COALESCE(
        (SELECT MAX(indice) FROM imagen WHERE obra_id = NEW.obra_id), 
        -1
    ) + 1;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_assign_indice
BEFORE INSERT ON imagen
FOR EACH ROW
EXECUTE FUNCTION assign_indice();
