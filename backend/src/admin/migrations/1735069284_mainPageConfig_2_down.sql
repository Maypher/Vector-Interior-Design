ALTER TABLE imagen DROP COLUMN IF EXISTS pagina_principal;
DROP SEQUENCE pag_principal_indice_seq CASCADE;
DROP TABLE IF EXISTS imagenConfig;
DROP TYPE IF EXISTS ubicacion;
