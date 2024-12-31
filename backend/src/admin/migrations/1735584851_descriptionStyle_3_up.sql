ALTER TABLE imagenConfig 
ADD COLUMN descripcionTipografia VARCHAR(50) NOT NULL DEFAULT 'Arial',
ADD COLUMN descripcionTamano FLOAT NOT NULL DEFAULT 1.0,
ADD COLUMN descripcionDistribucion VARCHAR(50) DEFAULT 'text-justify'
