import pytest
from mimesis.locales import Locale
from mimesis.schema import Field
from sanic_testing.testing import SanicASGITestClient
from sanic.request import Request, File
from sanic_testing.testing import (
    TestingResponse as Response,
)  # Using alias because pytest falsy discovers it
from admin.resources.resource_manager import AdminResourceManager
from common.common_graphql import schemas
from admin.resources.admin_graphql import Query, Mutation
from strawberry import Schema

project_count = 20
space_count = 10
image_count = 40


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
class TestProject:
    async def create_project(
        self, name: str, description: str, area: int, test_client: SanicASGITestClient
    ) -> int:
        """Creates a new project returning the ID."""

        mutation = """
            mutation createProject($name: String!, $description: String!, $area: Int!) {
                createProject(name: $name, description: $description, area: $area) {
                    id
                }
            }
        """

        variables = {
            "name": name,
            "description": description,
            "area": area,
        }

        create_res: Response
        query_res: Response

        _, create_res = await test_client.post(
            "/graphql", json={"query": mutation, "variables": variables}
        )
        return create_res.json["data"]["createProject"]["id"]

    @pytest.mark.asyncio
    async def test_create(
        self,
        test_client: SanicASGITestClient,
        mimesis: Field,
        admin_resource_manager: AdminResourceManager,
    ):
        query = """
            mutation createProject($name: String!, $description: String!, $area: Int!) {
                createProject(name: $name, description: $description, area: $area) {
                    name
                    description
                    area
                    public
                    thumbnail {
                        filename
                    }
                }
            }
        """

        variables = {
            "name": mimesis("word"),
            "description": mimesis("text"),
            "area": mimesis("integer_number", start=100, end=1000),
        }

        response: Response

        _, response = await test_client.post(
            "/graphql", json={"query": query, "variables": variables}
        )

        assert response.status == 200
        assert response.json.get("errors") is None
        assert response.json["data"]["createProject"] == {
            **variables,
            "public": False,
            "thumbnail": None,
        }

    @pytest.mark.asyncio
    async def test_get_project_by_id(
        self,
        test_client: SanicASGITestClient,
        mimesis: Field,
        admin_resource_manager: AdminResourceManager,
    ):
        query = """
            query Project($id: Int!) {
                project(id: $id) {
                    name
                    description
                    area
                }
            }
        """

        variables = {
            "name": mimesis("word"),
            "description": mimesis("text"),
            "area": mimesis("integer_number", start=100, end=1000),
        }

        created_id = await self.create_project(
            **variables,
            test_client=test_client,
        )

        query_res: Response

        _, query_res = await test_client.post(
            "/graphql", json={"query": query, "variables": {"id": created_id}}
        )

        assert query_res.json.get("errors") is None
        assert query_res.json["data"]["project"] == variables

    @pytest.mark.asyncio
    async def test_projct_delete(
        self,
        test_client: SanicASGITestClient,
        mimesis: Field,
        admin_resource_manager: AdminResourceManager,
    ):
        query = """
            query Project($id: Int!) {
                project(id: $id) {
                    id
                }
            }
        """

        delete_query = """
            mutation deleteProject($id: Int!) {
                deleteProject(id: $id)
            }
        """

        project_id = await self.create_project(
            mimesis("word"),
            mimesis("text"),
            mimesis("integer_number", start=100, end=1000),
            test_client,
        )

        await test_client.post(
            "/graphql", json={"query": delete_query, "variables": {"id": project_id}}
        )

        query_res: Response

        _, query_res = await test_client.post(
            "/graphql", json={"query": query, "variables": {"id": project_id}}
        )

        assert query_res.json.get("errors") is None
        assert query_res.json["data"]["project"] is None

    @pytest.mark.asyncio
    async def test_project_update(
        self,
        test_client: SanicASGITestClient,
        mimesis: Field,
        admin_resource_manager: AdminResourceManager,
    ):
        original_variables = {
            "name": mimesis("word"),
            "description": mimesis("text"),
            "area": mimesis("integer_number", start=100, end=1000),
        }

        update_variables = {
            "name": mimesis("word"),
            "description": mimesis("text"),
            "area": mimesis("integer_number", start=100, end=1000),
        }

        project_id = await self.create_project(
            **original_variables,
            test_client=test_client,
        )

        update_query = """
            mutation updateProject($id: Int!, $name: String!, $description: String!, $area: Int!) {
                updateProject(id: $id, name: $name, description: $description, area: $area) {
                    id
                    name
                    description
                    area
                }
            }
        """

        res: Response
        _, res = await test_client.post(
            "/graphql",
            json={
                "query": update_query,
                "variables": {"id": project_id, **update_variables},
            },
        )
        assert res.json.get("errors") is None
        assert original_variables != update_variables
        assert res.json["data"]["updateProject"] == {
            "id": project_id,
            **update_variables,
        }

    @pytest.mark.asyncio
    async def test_project_update_thumbnail(
        self,
        test_client: SanicASGITestClient,
        image: File,
        mimesis: Field,
        admin_resource_manager: AdminResourceManager,
    ):
        project: schemas.Project = admin_resource_manager.create_project(
            mimesis("word"),
            mimesis("text"),
            mimesis(
                "integer_number",
                start=0,
                end=1000,
            ),
        )

        space = admin_resource_manager.create_space(
            project.id, mimesis("word"), mimesis("text")
        )

        created_image = await admin_resource_manager.create_image(
            image, mimesis("sentence"), space.id
        )

        admin_resource_manager.update_project(project.id, thumbnail=created_image.id)

        query = """
            mutation updateThumbnail($id: Int!, $thumbnail: Int!) {
                updateProject(id: $id, thumbnail: $thumbnail) {
                    thumbnail {
                        filename
                    }
                }
            }
        """

        variables = {"id": project.id, "thumbnail": created_image.id}

        res: Response
        _, res = await test_client.post(
            "/graphql", json={"query": query, "variables": variables}
        )

        assert res.json.get("errors") is None
        assert (
            res.json["data"]["updateProject"]["thumbnail"]["filename"]
            == created_image.filename
        )

    @pytest.mark.asyncio
    async def test_project_update_thumbnail_different_project(
        self,
        image: File,
        mimesis: Field,
        admin_resource_manager: AdminResourceManager,
    ):
        project = admin_resource_manager.create_project(
            mimesis("word"),
            mimesis("sentence"),
            mimesis("integer_number", start=1, end=1000),
        )

        random_image = await admin_resource_manager.create_image(
            image,
            mimesis("sentence"),
            mimesis("integer_number", start=1, end=space_count),
        )

        updated_project = admin_resource_manager.update_project(
            project.id, thumbnail=random_image.id
        )

        assert updated_project is None
