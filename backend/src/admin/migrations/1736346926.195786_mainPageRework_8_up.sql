-- This migration couples all rows that are exclusive to phone into a single type

CREATE TYPE main_page_phone_config AS (
    image_borders BIT(4),
    description_position "location",
    logo_position "location",
    logo_borders BIT(4),
    overflow BOOLEAN
);

ALTER TABLE main_page_config
DROP COLUMN image_border_n, DROP COLUMN image_border_s, DROP COLUMN image_border_e, DROP COLUMN image_border_w,
DROP COLUMN description_position, DROP COLUMN logo_position,
DROP COLUMN logo_border_n, DROP COLUMN logo_border_s, DROP COLUMN logo_border_e, DROP COLUMN logo_border_w,
DROP COLUMN overflow,
ADD COLUMN phone_config main_page_phone_config DEFAULT ROW(B'0000', NULL, NULL, B'0000', false)::main_page_phone_config;
