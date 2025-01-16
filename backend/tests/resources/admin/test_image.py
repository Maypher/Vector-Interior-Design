import pytest
from mimesis import Locale, Field
from sanic_testing.testing import SanicASGITestClient
from sanic.request import File
from admin.resources.resource_manager import AdminResourceManager
from sanic_testing.testing import TestingResponse as Response
import json
from pathlib import Path
from common.common_graphql import enums

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

    @pytest.mark.asyncio
    async def test_update_image(
        self,
        admin_resource_manager: AdminResourceManager,
        mimesis: Field,
        image: File,
        test_client: SanicASGITestClient,
    ):

        created_image = await admin_resource_manager.create_image(
            image,
            mimesis("sentence"),
            space_id=mimesis("integer_number", start=1, end=space_count),
        )

        query = """
            mutation updateImage($filename: String!, $altText: String, $description: String, 
            $descriptionFont: String, $mainPage: Boolean, $hideInProject: Boolean, $sculpture: Boolean) {
                updateImage(filename: $filename, altText: $altText, description: $description, 
                descriptionFont: $descriptionFont, mainPage: $mainPage, hideInProject: $hideInProject, sculpture: $sculpture) {
                    filename
                    altText
                    description
                    descriptionFont
                    mainPage
                    hideInProject
                    sculpture
                }
            }
        """

        variables = {
            "filename": created_image.filename,
            "altText": mimesis("sentence"),
            "description": mimesis("text"),
            "descriptionFont": mimesis("word"),
            "mainPage": mimesis("boolean"),
            "hideInProject": mimesis("boolean"),
            "sculpture": mimesis("boolean"),
        }

        res: Response
        _, res = await test_client.post(
            "/graphql", json={"query": query, "variables": variables}
        )

        assert res.json.get("errors") is None
        assert res.json["data"]["updateImage"] == variables

    @pytest.mark.asyncio
    async def test_update_image_no_values(
        self,
        admin_resource_manager: AdminResourceManager,
        mimesis: Field,
        image: File,
        test_client: SanicASGITestClient,
    ):
        created_image = await admin_resource_manager.create_image(
            image,
            mimesis("sentence"),
            space_id=mimesis("integer_number", start=1, end=space_count),
        )

        query = """
            mutation updateImage($filename: String!, $altText: String, $description: String, 
            $descriptionFont: String, $mainPage: Boolean, $hideInProject: Boolean, $sculpture: Boolean) {
                updateImage(filename: $filename, altText: $altText, description: $description, 
                descriptionFont: $descriptionFont, mainPage: $mainPage, hideInProject: $hideInProject, sculpture: $sculpture) {
                    filename
                    altText
                    description
                    descriptionFont
                    mainPage
                    hideInProject
                    sculpture
                }
            }
        """

        variables = {
            "filename": created_image.filename,
        }

        res: Response
        _, res = await test_client.post(
            "/graphql", json={"query": query, "variables": variables}
        )

        assert res.json.get("errors") is None
        assert res.json["data"]["updateImage"] == {
            "filename": created_image.filename,
            "altText": created_image.alt_text,
            "description": created_image.description,
            "descriptionFont": created_image.description_font,
            "mainPage": created_image.main_page,
            "hideInProject": created_image.hide_in_project,
            "sculpture": created_image.sculpture,
        }

    @pytest.mark.asyncio
    async def test_update_main_page_config(
        self,
        admin_resource_manager: AdminResourceManager,
        mimesis: Field,
        image: File,
        test_client: SanicASGITestClient,
    ):
        created_image = await admin_resource_manager.create_image(
            image,
            mimesis("sentence"),
            mimesis("integer_number", start=1, end=space_count),
        )
        created_image = admin_resource_manager.update_image(
            created_image.filename, main_page=True
        )

        main_page_query = """
            mutation updateImage($filename: String!, $mainPage: Boolean!) {
                updateImage(filename: $filename, mainPage: $mainPage) {
                    mainImageConfig {
                        id
                    }
                }
            }
        """
        variables = {
            "filename": created_image.filename,
            "mainPage": created_image.main_page,
        }

        updateRes: Response

        _, updateRes = await test_client.post(
            "/graphql", json={"query": main_page_query, "variables": variables}
        )

        page_config_id = updateRes.json["data"]["updateImage"]["mainImageConfig"]["id"]

        main_page_config_query = """
            mutation updateMainPageConfig($id: Int!, $descriptionEs: String, $descriptionEn: String, $descriptionFont: String, 
            $descriptionAlignment: String, $descriptionFontSize: Float, $phoneConfig: MainPageImagePhoneConfigInput, 
            $desktopConfig: MainPageImageDesktopConfigInput) {
                updateMainPageConfig(id: $id, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn, 
                descriptionFont: $descriptionFont, descriptionAlignment: $descriptionAlignment, descriptionFontSize: $descriptionFontSize,
                phoneConfig: $phoneConfig, desktopConfig: $desktopConfig) {
                    id
                    descriptionEs
                    descriptionEn
                    descriptionFont
                    descriptionAlignment
                    descriptionFontSize
                    phoneConfig {
                        imageBorders {
                            n
                            s
                            e
                            w
                        }
                        descriptionPosition
                        logoPosition
                        logoBorders {
                            n
                            s
                            e
                            w
                        }
                        overflow
                    }
                    desktopConfig {
                        imagePosition
                        descriptionPosition
                        descriptionBorders {
                            n
                            s
                            e
                            w
                        }
                        logoPosition
                        logoBorders {
                            n
                            s
                            e
                            w
                        }
                        overflow
                    }
                }
            }
        """

        locations = ["N", "S", "E", "W"]
        variables = {
            "id": page_config_id,
            "descriptionEs": mimesis("sentence"),
            "descriptionEn": mimesis("sentence"),
            "descriptionFont": mimesis("word"),
            "descriptionAlignment": mimesis("word"),
            "descriptionFontSize": mimesis("float_number"),
            "phoneConfig": {
                "imageBorders": {
                    "n": mimesis("boolean"),
                    "s": mimesis("boolean"),
                    "e": mimesis("boolean"),
                    "w": mimesis("boolean"),
                },
                "descriptionPosition": mimesis("choice", items=locations),
                "logoPosition": mimesis("choice", items=locations),
                "logoBorders": {
                    "n": mimesis("boolean"),
                    "s": mimesis("boolean"),
                    "e": mimesis("boolean"),
                    "w": mimesis("boolean"),
                },
                "overflow": mimesis("boolean"),
            },
            "desktopConfig": {
                "imagePosition": mimesis("choice", items=["LEFT", "RIGHT", "CENTER"]),
                "descriptionPosition": mimesis("choice", items=locations),
                "descriptionBorders": {
                    "n": mimesis("boolean"),
                    "s": mimesis("boolean"),
                    "e": mimesis("boolean"),
                    "w": mimesis("boolean"),
                },
                "logoPosition": mimesis("choice", items=locations),
                "logoBorders": {
                    "n": mimesis("boolean"),
                    "s": mimesis("boolean"),
                    "e": mimesis("boolean"),
                    "w": mimesis("boolean"),
                },
                "overflow": mimesis("boolean"),
            },
        }

        res: Response

        _, res = await test_client.post(
            "/graphql", json={"query": main_page_config_query, "variables": variables}
        )

        assert res.json.get("errors") is None
        assert res.json["data"]["updateMainPageConfig"] == variables
