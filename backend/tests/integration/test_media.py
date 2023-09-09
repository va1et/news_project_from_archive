import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

import tests.models as test_models
from tests.integration.utils import create_base_media, create_random_media


class TestMedia:
    @classmethod
    async def check_system(cls, body: dict) -> None:
        assert "guid" in body.keys()
        assert "is_deleted" in body.keys()
        assert "created_at" in body.keys()
        assert "updated_at" in body.keys()

    @pytest.mark.asyncio
    async def test_get_medias(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_media(client=client, headers=headers)

        response = await client.get("/media", headers=headers)
        assert response.status_code == 200

        medias = response.json()
        assert len(medias) == 10

    @pytest.mark.asyncio
    async def test_get_medias_bad_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_media(client=client, headers=headers)
        mocker.stop(auth_mocker)
        response = await client.get("/media", headers=headers)
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_medias_no_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        for _ in range(10):
            await create_random_media(client=client, headers=headers)
        response = await client.get("/media", headers=None)
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_media(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        media = await create_base_media(client=client, headers=headers)
        response = await client.get(f"/media/{media['guid']}", headers=headers)
        assert response.status_code == 200

        media = response.json()
        assert media["link"] == test_models.MEDIA_CREATE_LINK
        await self.check_system(media)

    @pytest.mark.asyncio
    async def test_post_media(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        response = await client.post("/media", headers=headers, json=jsonable_encoder(test_models.MEDIA_CREATE))
        assert response.status_code == 201

        media = response.json()
        assert media["link"] == test_models.MEDIA_CREATE_LINK
        await self.check_system(media)

    @pytest.mark.asyncio
    async def test_put_media(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        media = await create_base_media(client=client, headers=headers)
        response = await client.put(
            f"/media/{media['guid']}", headers=headers, json=jsonable_encoder(test_models.MEDIA_PUT)
        )
        assert response.status_code == 200

        media = response.json()
        assert media["link"] == test_models.MEDIA_PUT_LINK
        await self.check_system(media)

    @pytest.mark.asyncio
    async def test_delete_media(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        media = await create_base_media(client=client, headers=headers)
        response = await client.delete(f"/media/{media['guid']}", headers=headers)
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_patch_media(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
        media = await create_base_media(client=client, headers=headers)
        response = await client.patch(
            f"/media/{media['guid']}",
            headers=headers,
            json=jsonable_encoder(test_models.MEDIA_PATCH, exclude_unset=True),
        )
        assert response.status_code == 200

        media = response.json()
        assert media["link"] == test_models.MEDIA_PATCH_LINK
        await self.check_system(media)
