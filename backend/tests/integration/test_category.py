import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

import tests.models as test_models
from tests.integration.utils import create_base_category, create_random_category


class TestCategory:
    @classmethod
    async def check_system(cls, body: dict) -> None:
        assert "guid" in body.keys()
        assert "is_deleted" in body.keys()
        assert "created_at" in body.keys()
        assert "updated_at" in body.keys()

    @pytest.mark.asyncio
    async def test_get_categories(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_category(client=client, headers=headers)

        response = await client.get("/category", headers=headers)
        assert response.status_code == 200

        categories = response.json()
        assert len(categories) == 10

    @pytest.mark.asyncio
    async def test_get_categories_bad_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_category(client=client, headers=headers)
        mocker.stop(auth_mocker)
        response = await client.get("/category", headers=headers)
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_categories_no_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_category(client=client, headers=headers)
        response = await client.get("/category", headers=None)
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_category(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        category = await create_base_category(client=client, headers=headers)
        response = await client.get(f"/category/{category['guid']}", headers=headers)
        assert response.status_code == 200

        category = response.json()
        assert category["name"] == test_models.CATEGORY_CREATE_NAME
        await self.check_system(category)

    @pytest.mark.asyncio
    async def test_post_category(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        response = await client.post("/category", headers=headers, json=jsonable_encoder(test_models.CATEGORY_CREATE))
        assert response.status_code == 201

        category = response.json()
        assert category["name"] == test_models.CATEGORY_CREATE_NAME
        await self.check_system(category)

    @pytest.mark.asyncio
    async def test_put_category(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        category = await create_base_category(client=client, headers=headers)
        response = await client.put(
            f"/category/{category['guid']}", headers=headers, json=jsonable_encoder(test_models.CATEGORY_PUT)
        )
        assert response.status_code == 200

        category = response.json()
        assert category["name"] == test_models.CATEGORY_PUT_NAME
        await self.check_system(category)

    @pytest.mark.asyncio
    async def test_delete_category(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        category = await create_base_category(client=client, headers=headers)
        response = await client.delete(f"/category/{category['guid']}", headers=headers)
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_patch_category(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        category = await create_base_category(client=client, headers=headers)
        response = await client.patch(
            f"/category/{category['guid']}",
            headers=headers,
            json=jsonable_encoder(test_models.CATEGORY_PATCH, exclude_unset=True),
        )
        assert response.status_code == 200

        category = response.json()
        assert category["name"] == test_models.CATEGORY_PATCH_NAME
        await self.check_system(category)
