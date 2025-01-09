ALTER TABLE main_page_config
DROP COLUMN phone_config,
ADD COLUMN image_border_n BOOLEAN DEFAULT false,
ADD COLUMN image_border_s BOOLEAN DEFAULT false,
ADD COLUMN image_border_e BOOLEAN DEFAULT false,
ADD COLUMN image_border_w BOOLEAN DEFAULT false,
ADD COLUMN description_position BOOLEAN DEFAULT NULL,
ADD COLUMN logo_position BOOLEAN DEFAULT NULL,
ADD COLUMN logo_border_n BOOLEAN DEFAULT false,
ADD COLUMN logo_border_s BOOLEAN DEFAULT false,
ADD COLUMN logo_border_e BOOLEAN DEFAULT false,
ADD COLUMN logo_border_w BOOLEAN DEFAULT false,
ADD COLUMN overflow BOOLEAN DEFAULT false;

DROP TYPE main_page_phone_config;
