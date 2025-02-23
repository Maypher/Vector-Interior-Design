ALTER TABLE project RENAME COLUMN description_es TO description;
ALTER TABLE project DROP COLUMN description_en;

ALTER TABLE space RENAME COLUMN description_es TO description;
ALTER TABLE space DROP COLUMN description_en;

ALTER TABLE image RENAME COLUMN description_es TO description;
ALTER TABLE image DROP COLUMN description_en;
ALTER TABLE image RENAME alt_text_es TO alt_text;
ALTER TABLE image DROP COLUMN alt_text_en;
