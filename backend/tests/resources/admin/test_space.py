import pytest
from mimesis.locales import Locale
from mimesis.schema import Field
from sanic_testing.testing import SanicASGITestClient
from sanic.request import Request
from sanic_testing.testing import (
    TestingResponse as Response,
)  # Using alias because pytest falsy discovers it
from admin.resources.resource_manager import AdminResourceManager


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
class TestSpace:
    @pytest.mark.asyncio
    async def test_space_create(
        self, test_client: SanicASGITestClient, mimesis: Field, admin_resource_manager
    ):
        project_id = mimesis("integer_number", start=1, end=project_count)

        mutation = """
            mutation createSpace($projectId: Int!, $name: String!, $description: String!) {
                createSpace(projectId: $projectId, name: $name, description: $description) {
                    __typename
                    ... on Space {
                        name
                        description
                        project {
                            id
                        }
                    }
                    ... on ProjectNotFoundSpace {
                        projectId
                    }
                }
            }
        """

        space_name = mimesis("word")
        space_description = mimesis("text")

        variables = {
            "projectId": project_id,
            "name": space_name,
            "description": space_description,
        }

        res: Response

        _, res = await test_client.post(
            "/graphql", json={"query": mutation, "variables": variables}
        )

        assert res.json.get("errors") is None
        assert res.json["data"]["createSpace"]["__typename"] == "Space"
        assert res.json["data"]["createSpace"] == {
            "__typename": "Space",
            "name": space_name,
            "description": space_description,
            "project": {"id": project_id},
        }

    @pytest.mark.asyncio
    async def test_space_create_invalid_project(
        self,
        mimesis: Field,
        test_client: SanicASGITestClient,
        admin_resource_manager: AdminResourceManager,
    ):
        project_id = 0

        mutation = """
            mutation createSpace($projectId: Int!, $name: String!, $description: String!) {
                createSpace(projectId: $projectId, name: $name, description: $description) {
                    __typename
                    ... on Space {
                        name
                        description
                        project {
                            id
                        }
                    }
                    ... on ProjectNotFoundSpace {
                        projectId
                    }
                }
            }
        """

        space_name = mimesis("word")
        space_description = mimesis("text")

        variables = {
            "projectId": project_id,
            "name": space_name,
            "description": space_description,
        }

        res: Response

        _, res = await test_client.post(
            "/graphql", json={"query": mutation, "variables": variables}
        )

        assert res.json.get("errors") is None
        assert res.json["data"]["createSpace"]["__typename"] == "ProjectNotFoundSpace"
        assert res.json["data"]["createSpace"]["projectId"] == project_id

    @pytest.mark.asyncio
    async def test_query_space(
        self,
        test_client: SanicASGITestClient,
        mimesis: Field,
        admin_resource_manager: AdminResourceManager,
    ):
        project_id = mimesis("integer_number", start=1, end=project_count)
        project_name = mimesis("word")
        project_description = mimesis("text")

        space = admin_resource_manager.create_space(
            project_id, project_name, project_description
        )

        query = """
            query space($id: Int!) {
                space(id: $id) {
                    name
                    description
                }
            }
        """

        res: Response
        _, res = await test_client.post(
            "/graphql",
            json={
                "query": query,
                "variables": {
                    "id": space.id,
                    "name": project_name,
                    "description": project_description,
                },
            },
        )

        assert res.json.get("errors") is None
        assert res.json["data"]["space"] == {
            "name": project_name,
            "description": project_description,
        }

    @pytest.mark.asyncio
    async def test_update_space(
        self,
        test_client: SanicASGITestClient,
        mimesis: Field,
        admin_resource_manager: AdminResourceManager,
    ):
        space_id = mimesis("integer_number", start=1, end=space_count)
        space = admin_resource_manager.get_space_by_id(space_id)

        query = """
            mutation updateSpace($id: Int!, $name: String, $description: String) {
                updateSpace(id: $id, name: $name, description: $description) {
                    id
                    name
                    description
                }
            }
        """

        variables = {
            "id": space.id,
            "name": mimesis("word"),
            "description": mimesis("text"),
        }

        res: Response
        _, res = await test_client.post(
            "/graphql", json={"query": query, "variables": variables}
        )

        assert res.json.get("errors") is None
        assert res.json["data"]["updateSpace"] == variables
        assert res.json["data"]["updateSpace"]["name"] != space.name
        assert res.json["data"]["updateSpace"]["description"] != space.description

    @pytest.mark.asyncio
    async def test_update_space_no_values(
        self,
        test_client: SanicASGITestClient,
        mimesis: Field,
        admin_resource_manager: AdminResourceManager,
    ):
        space_id = mimesis("integer_number", start=1, end=space_count)
        space = admin_resource_manager.get_space_by_id(space_id)

        admin_resource_manager.update_space(space_id, None, None, None)

        query = """
            mutation updateSpace($id: Int!, $name: String, $description: String, $index: Int) {
                updateSpace(id: $id, name: $name, description: $description, index: $index) {
                    id
                    name
                    description
                }
            }
        """

        variables = {"id": space.id, "name": None, "description": None, "index": None}

        res: Response
        _, res = await test_client.post(
            "/graphql", json={"query": query, "variables": variables}
        )

        assert res.json.get("errors") is None
        assert res.json["data"]["updateSpace"] == {
            "id": space.id,
            "name": space.name,
            "description": space.description,
        }

    @pytest.mark.asyncio
    async def test_delete_space(
        self,
        test_client: SanicASGITestClient,
        mimesis: Field,
        admin_resource_manager: AdminResourceManager,
    ):
        space_id = mimesis("integer_number", start=1, end=space_count)

        mutation = """
            mutation deleteSpace($id: Int!) {
                deleteSpace(id: $id)
            }
        """

        res: Response
        _, res = await test_client.post(
            "/graphql", json={"query": mutation, "variables": {"id": space_id}}
        )

        assert res.json.get("errors") is None
        assert res.json["data"]["deleteSpace"] is True
        assert admin_resource_manager.get_space_by_id(space_id) is None
