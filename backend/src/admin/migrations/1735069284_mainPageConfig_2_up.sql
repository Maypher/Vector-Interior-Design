-- Used to mark that an image should be shown in the main screen of the website.
ALTER TABLE imagen ADD COLUMN IF NOT EXISTS pagina_principal BOOLEAN DEFAULT FALSE;

CREATE SEQUENCE pag_principal_indice_seq;

CREATE TYPE ubicacion AS ENUM ('N', 'S', 'E', 'O');

CREATE TABLE IF NOT EXISTS imagenConfig (
    id SERIAL PRIMARY KEY,
    imagen_id INTEGER REFERENCES imagen(id) ON DELETE CASCADE,
    imagen_borde_n BOOLEAN DEFAULT false,
    imagen_borde_s BOOLEAN DEFAULT false,
    imagen_borde_e BOOLEAN DEFAULT false,
    imagen_borde_o BOOLEAN DEFAULT false,
    descripcion TEXT,
    descripcion_en TEXT,
    texto_ubicacion ubicacion DEFAULT NULL,
    logo_ubicacion ubicacion DEFAULT NULL,
    logo_borde_n BOOLEAN DEFAULT false,
    logo_borde_s BOOLEAN DEFAULT false,
    logo_borde_e BOOLEAN DEFAULT false,
    logo_borde_o BOOLEAN DEFAULT false,
    sangrar BOOLEAN DEFAULT false,
    indice FLOAT NOT NULL DEFAULT nextval('pag_principal_indice_seq')::FLOAT
);
