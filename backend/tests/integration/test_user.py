import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

import tests.models as test_models
from tests.integration.utils import create_base_user, create_random_user


class TestUser:
    @classmethod
    async def check_system(cls, body: dict) -> None:
        assert "guid" in body.keys()
        assert "is_deleted" in body.keys()
        assert "created_at" in body.keys()
        assert "updated_at" in body.keys()

    @pytest.mark.asyncio
    async def test_get_users(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_user(client=client, headers=headers)

        response = await client.get("/user", headers=headers)
        assert response.status_code == 200

        users = response.json()
        assert len(users) == 10

    @pytest.mark.asyncio
    async def test_get_users_bad_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_user(client=client, headers=headers)
        mocker.stop(auth_mocker)
        response = await client.get("/user", headers=headers)
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_users_no_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_user(client=client, headers=headers)
        response = await client.get("/user", headers=None)
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_user(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        user = await create_base_user(client=client, headers=headers)
        response = await client.get(f"/user/{user['guid']}", headers=headers)
        assert response.status_code == 200

        user = response.json()
        assert user["email"] == test_models.USER_CREATE_EMAIL
        assert user["first_name"] == test_models.USER_CREATE_FIRST_NAME
        assert user["last_name"] == test_models.USER_CREATE_LAST_NAME
        assert user["middle_name"] == test_models.USER_CREATE_MIDDLE_NAME
        assert user["role"] == test_models.USER_CREATE_ROLE
        await self.check_system(user)

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        user = await create_base_user(client=client, headers=headers)
        response = await client.get(f"/user/email/{user['email']}", headers=headers)
        assert response.status_code == 200

        user = response.json()
        assert user["email"] == test_models.USER_CREATE_EMAIL
        assert user["first_name"] == test_models.USER_CREATE_FIRST_NAME
        assert user["last_name"] == test_models.USER_CREATE_LAST_NAME
        assert user["middle_name"] == test_models.USER_CREATE_MIDDLE_NAME
        assert user["role"] == test_models.USER_CREATE_ROLE
        await self.check_system(user)

    @pytest.mark.asyncio
    async def test_post_user(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        response = await client.post("/user", headers=headers, json=jsonable_encoder(test_models.USER_CREATE))
        assert response.status_code == 201

        user = response.json()
        assert user["email"] == test_models.USER_CREATE_EMAIL
        assert user["first_name"] == test_models.USER_CREATE_FIRST_NAME
        assert user["last_name"] == test_models.USER_CREATE_LAST_NAME
        assert user["middle_name"] == test_models.USER_CREATE_MIDDLE_NAME
        assert user["role"] == test_models.USER_CREATE_ROLE
        await self.check_system(user)

    @pytest.mark.asyncio
    async def test_put_user(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        user = await create_base_user(client=client, headers=headers)
        response = await client.put(
            f"/user/{user['guid']}", headers=headers, json=jsonable_encoder(test_models.USER_PUT)
        )
        assert response.status_code == 200

        user = response.json()
        assert user["email"] == test_models.USER_PUT_EMAIL
        assert user["first_name"] == test_models.USER_PUT_FIRST_NAME
        assert user["last_name"] == test_models.USER_PUT_LAST_NAME
        assert user["middle_name"] == test_models.USER_PUT_MIDDLE_NAME
        assert user["role"] == test_models.USER_PUT_ROLE
        await self.check_system(user)

    @pytest.mark.asyncio
    async def test_delete_user(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        user = await create_base_user(client=client, headers=headers)
        response = await client.delete(f"/user/{user['guid']}", headers=headers)
        assert response.status_code == 204

        response = await client.get(f"/user/{user['guid']}", headers=headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_patch_user(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        user = await create_base_user(client=client, headers=headers)
        response = await client.patch(
            f"/user/{user['guid']}",
            headers=headers,
            json=jsonable_encoder(test_models.USER_PATCH, exclude_unset=True),
        )
        assert response.status_code == 200

        user = response.json()
        assert user["email"] == test_models.USER_PATCH_EMAIL
        await self.check_system(user)
