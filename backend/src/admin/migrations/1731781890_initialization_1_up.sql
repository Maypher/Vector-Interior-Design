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

CREATE SEQUENCE obra_indice_seq;

CREATE TABLE public.obra (
    id SMALLSERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    area INT NOT NULL,
    indice FLOAT NOT NULL DEFAULT nextval('obra_indice_seq')::FLOAT,
    publico BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT unique_indice UNIQUE (indice) DEFERRABLE INITIALLY DEFERRED
);

CREATE SEQUENCE ambiente_indice_seq;

CREATE TABLE public.ambiente (
    id SMALLSERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    obra_id INTEGER REFERENCES obra ON DELETE CASCADE,
    indice FLOAT NOT NULL DEFAULT nextval('ambiente_indice_seq')::FLOAT,
    CONSTRAINT repeated_index_ambiente UNIQUE (obra_id, indice) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT repeated_name UNIQUE (obra_id, nombre)
);

CREATE SEQUENCE imagen_indice_seq;

CREATE TABLE public.imagen (
    id SMALLSERIAL PRIMARY KEY,
    archivo VARCHAR(255) UNIQUE NOT NULL,
    texto_alt VARCHAR(255) NOT NULL,
    indice FLOAT NOT NULL DEFAULT nextval('imagen_indice_seq')::FLOAT,
    ambiente_id INTEGER REFERENCES ambiente ON DELETE CASCADE,
    CONSTRAINT repeated_index_image UNIQUE (ambiente_id, indice) DEFERRABLE INITIALLY DEFERRED
);

-- Done this way because of circular dependencies
ALTER TABLE public.obra ADD COLUMN imagen_principal INTEGER REFERENCES imagen;

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
