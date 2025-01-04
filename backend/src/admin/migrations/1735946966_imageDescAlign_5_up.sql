ALTER TYPE imagenTlfnConfig ADD ATTRIBUTE descripcionAlineacion VARCHAR(50);
ALTER TABLE imagen ALTER COLUMN tlfnConfig SET DEFAULT ROW(B'0000', 'CENTRO', NULL, 'text-justify');
