import pytest
from mimesis import Locale, Field
from sanic_testing.testing import SanicASGITestClient
from sanic.request import File
from admin.resources.resource_manager import AdminResourceManager
from sanic_testing.testing import TestingResponse as Response
import json

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
                    altText
                }
            }
        """

        variables = {"spaceId": space_id, "image": None, "altText": alt_text}

        operations = {"query": query, "variables": variables}
        form_map = {"image": ["variables.image"]}

        res: Response

        # TODO: Figure out why it returns 400 unsupported content type
        _, res = await test_client.post(
            "/graphql",
            data={"operations": operations, "map": form_map},
            files={"image": image.body},
        )

        assert res.json.get("errors") is None
        assert res.json["data"]["createImage"] == {"altText": alt_text}
