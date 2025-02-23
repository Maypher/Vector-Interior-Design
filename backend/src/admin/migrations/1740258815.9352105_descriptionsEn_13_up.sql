ALTER TABLE project RENAME COLUMN description TO description_es;
ALTER TABLE project ADD COLUMN description_en TEXT NOT NULL DEFAULT '';

ALTER TABLE space RENAME COLUMN description TO description_es;
ALTER TABLE space ADD COLUMN description_en TEXT DEFAULT '';

ALTER TABLE image RENAME COLUMN description TO description_es;
ALTER TABLE image ADD COLUMN description_en TEXT DEFAULT '';
ALTER TABLE image RENAME COLUMN alt_text TO alt_text_es;
ALTER TABLE image ADD COLUMN alt_text_en VARCHAR(255) NOT NULL DEFAULT '';
