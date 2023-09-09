import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

import tests.models as test_models
from tests.integration.utils import create_base_comment, create_random_comment


class TestComment:
    @classmethod
    async def check_system(cls, body: dict) -> None:
        assert "guid" in body.keys()
        assert "is_deleted" in body.keys()
        assert "created_at" in body.keys()
        assert "updated_at" in body.keys()

    @pytest.mark.asyncio
    async def test_get_comments(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_comment(client=client, headers=headers)

        response = await client.get("/comment", headers=headers)
        assert response.status_code == 200

        comments = response.json()
        assert len(comments) == 10

    @pytest.mark.asyncio
    async def test_get_comments_bad_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_comment(client=client, headers=headers)
        mocker.stop(auth_mocker)
        response = await client.get("/comment", headers=headers)
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_comments_no_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_comment(client=client, headers=headers)
        response = await client.get("/comment", headers=None)
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_comment(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        comment = await create_base_comment(client=client, headers=headers)
        response = await client.get(f"/comment/{comment['guid']}", headers=headers)
        assert response.status_code == 200

        comment = response.json()
        assert comment["text"] == test_models.COMMENT_CREATE_TEXT
        await self.check_system(comment)

    @pytest.mark.asyncio
    async def test_post_comment(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        response = await client.post("/comment", headers=headers, json=jsonable_encoder(test_models.COMMENT_CREATE))
        assert response.status_code == 201

        comment = response.json()
        assert comment["text"] == test_models.COMMENT_CREATE_TEXT
        await self.check_system(comment)

    @pytest.mark.asyncio
    async def test_put_comment(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        comment = await create_base_comment(client=client, headers=headers)
        response = await client.put(
            f"/comment/{comment['guid']}", headers=headers, json=jsonable_encoder(test_models.COMMENT_PUT)
        )
        assert response.status_code == 200

        comment = response.json()
        assert comment["text"] == test_models.COMMENT_PUT_TEXT
        await self.check_system(comment)

    @pytest.mark.asyncio
    async def test_delete_comment(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        comment = await create_base_comment(client=client, headers=headers)
        response = await client.delete(f"/comment/{comment['guid']}", headers=headers)
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_patch_comment(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        comment = await create_base_comment(client=client, headers=headers)
        response = await client.patch(
            f"/comment/{comment['guid']}",
            headers=headers,
            json=jsonable_encoder(test_models.COMMENT_PATCH, exclude_unset=True),
        )
        assert response.status_code == 200

        comment = response.json()
        assert comment["text"] == test_models.COMMENT_PATCH_TEXT
        await self.check_system(comment)
