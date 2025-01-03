CREATE TYPE alineacionImagen AS ENUM ('IZQUIERDA', 'DERECHA', 'CENTRO', 'SANGRAR');

CREATE TYPE imagenTlfnConfig AS (
    bordes BIT(4), -- 4 bits that identify the borders of the image in the order n, s, e, w
    alineacion alineacionImagen,
    descripcionUbicacion ubicacion
);

ALTER TABLE imagen ADD COLUMN tlfnConfig imagenTlfnConfig DEFAULT ROW(B'0000', 'CENTRO', NULL),
ADD COLUMN descripcion TEXT;
