ALTER TABLE image
DROP COLUMN IF EXISTS sculpture;

DROP TABLE IF EXISTS sculpture_data;
DROP SEQUENCE IF EXISTS sculpture_index_seq;
