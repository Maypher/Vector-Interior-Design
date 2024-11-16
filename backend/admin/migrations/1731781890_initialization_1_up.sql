CREATE TABLE administration.usuario (
    id INTEGER PRIMARY KEY,
    email VARCHAR(75) UNIQUE NOT NULL,
    password_hash VARCHAR(75) NOT NULL
);

CREATE TABLE public.obra (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL
);

CREATE TABLE public.imagen (
    id INTEGER PRIMARY KEY,
    archivo VARCHAR(255) UNIQUE NOT NULL,
    texto_alt VARCHAR(255) NOT NULL,
    obra_id INTEGER REFERENCES obra ON DELETE CASCADE
);
