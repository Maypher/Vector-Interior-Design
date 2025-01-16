CREATE TYPE main_page_image_position AS ENUM ('LEFT', 'RIGHT', 'CENTER');

CREATE TYPE main_page_desktop_config AS (
    image_position main_page_image_position,
    description_position location,
    description_borders BIT(4),
    logo_position location,
    logo_borders BIT(4),
    description_logo_position location,
    description_logo_borders BIT(4),
    overflow BOOLEAN
);

ALTER TABLE main_page_config ADD COLUMN desktop_config main_page_desktop_config 
DEFAULT ROW('CENTER', NULL, B'0000', NULL, B'0000', NULL, B'0000', false)::main_page_desktop_config;
