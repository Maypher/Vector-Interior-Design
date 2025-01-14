import pytest
from mimesis import Locale, Field
from sanic_testing.testing import SanicASGITestClient
from sanic.request import File
from admin.resources.resource_manager import AdminResourceManager
from sanic_testing.testing import TestingResponse as Response
import json
from pathlib import Path

project_count = 50
space_count = 20
image_count = 30


@pytest.mark.parametrize("mimesis_locale", [Locale.ES])
@pytest.mark.parametrize(
    "admin_resource_manager",
    [
        {
            "project_count": project_count,
            "space_count": space_count,
            "image_count": image_count,
        }
    ],
    indirect=True,
)
class TestImage:
    @pytest.mark.asyncio
    async def test_create_image(
        self,
        mimesis: Field,
        test_client: SanicASGITestClient,
        admin_resource_manager: AdminResourceManager,
        image: File,
    ):
        space_id = mimesis("integer_number", start=1, end=space_count)
        alt_text = mimesis("sentence")

        query = """
            mutation createImage($spaceId: Int!, $image: Upload!, $altText: String!) {
                createImage(spaceId: $spaceId, image: $image, altText: $altText) {
                    __typename
                    ... on Image {
                        filename
                        altText 
                    }
                    ... on SpaceNotFoundImage {
                        spaceId
                    }
                    ... on UnsupportedFileType {
                        filetype
                    }
                }
            }
        """

        variables = {"spaceId": space_id, "image": None, "altText": alt_text}

        operations = {"query": query, "variables": variables}
        form_map = {"image": ["variables.image"]}

        res: Response

        _, res = await test_client.post(
            "/graphql",
            data={"operations": json.dumps(operations), "map": json.dumps(form_map)},
            files={"image": (image.name, image.body, image.type)},
        )

        assert res.json.get("errors") is None
        data = res.json["data"]["createImage"]

        assert data["__typename"] == "Image"
        assert data["altText"] == alt_text
        assert Path(f"/storage/images/{data["filename"]}").is_file()

    @pytest.mark.asyncio
    async def test_delete_image(
        self, admin_resource_manager: AdminResourceManager, mimesis: Field, image: File
    ):
        image = await admin_resource_manager.create_image(
            image,
            mimesis("sentence"),
            mimesis("integer_number", start=1, end=space_count),
        )

        admin_resource_manager.delete_image(image.filename)

        assert admin_resource_manager.get_image_by_filename(image.filename) is None
