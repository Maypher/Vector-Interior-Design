import pytest
from mimesis.locales import Locale
from mimesis.schema import Field
from sanic_testing.testing import SanicASGITestClient
from sanic.request import Request
from sanic_testing.testing import (
    TestingResponse as Response,
)  # Using alias because pytest falsy discovers it


@pytest.mark.parametrize("mimesis_locale", [Locale.ES])
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
    async def test_create(self, test_client: SanicASGITestClient, mimesis: Field):
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
