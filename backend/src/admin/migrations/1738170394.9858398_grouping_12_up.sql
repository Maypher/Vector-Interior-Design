-- The logic behind this method is that when it finds an image with group position it
-- will continue until an image without a group position is found and that will be the end of a group.
CREATE TYPE image_group_alignment AS ENUM ('TOP', 'MIDDLE', 'BOTTOM');

CREATE TYPE image_desktop_config AS (
    group_alignment image_group_alignment,
    image_size INT,
    image_borders BIT(4),
    description_position location,
    description_borders BIT(4),
    description_logo_position location,
    logo_position location,
    logo_borders BIT(4)
);

ALTER TABLE image ADD COLUMN desktop_config image_desktop_config DEFAULT 
ROW('MIDDLE', 100, B'0000', NULL, B'0000', NULL, NULL, B'0000')::image_desktop_config;
