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
    obra_id INTEGER REFERENCES obra ON DELETE CASCADE
);
