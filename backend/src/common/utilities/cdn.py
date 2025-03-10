import cloudinary


def gen_image_url(image_id: str, watermark: bool = True) -> str:
    image_url = cloudinary.CloudinaryImage(image_id).build_url(
        sign_url=True,
        transformations=(
            [
                {
                    "overlay": "watermark",
                    "width": 0.7,
                    "opacity": 50,
                    "gravity": "south_east",
                    "x": -0.05,
                    "y": -0.05,
                }
            ]
            if watermark
            else None
        ),
    )

    return image_url
