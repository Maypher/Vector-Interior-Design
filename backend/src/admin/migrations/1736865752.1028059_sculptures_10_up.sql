ALTER TABLE image
ADD COLUMN sculpture BOOLEAN DEFAULT false;

CREATE SEQUENCE sculpture_index_seq;
CREATE TABLE sculpture_data (
    id SERIAL PRIMARY KEY,
    image_id INTEGER UNIQUE REFERENCES image(id) ON DELETE CASCADE,
    description_es TEXT,
    description_en TEXT,
    index FLOAT DEFAULT nextval('sculpture_index_seq')::FLOAT
);
