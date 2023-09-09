# import pytest
# from fastapi.encoders import jsonable_encoder
# from httpx import AsyncClient
#
# import tests.models as test_models
# from tests.integration.utils import create_base_news, create_random_news
#
#
# class TestRecord:
#     @classmethod
#     async def check_system(cls, body: dict) -> None:
#         assert "guid" in body.keys()
#         assert "is_deleted" in body.keys()
#         assert "created_at" in body.keys()
#         assert "updated_at" in body.keys()
#
#     @pytest.mark.asyncio
#     async def test_get_multiple_news(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
#         for _ in range(10):
#             await create_random_news(client=client, headers=headers)
#
#         response = await client.get("/news", headers=headers)
#         assert response.status_code == 200
#
#         news = response.json()
#         assert len(news) == 10
#
#     @pytest.mark.asyncio
#     async def test_get_news_multiple_bad_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
#         for _ in range(10):
#             await create_random_news(client=client, headers=headers)
#         mocker.stop(auth_mocker)
#         response = await client.get("/news", headers=headers)
#         assert response.status_code == 401
#
#     @pytest.mark.asyncio
#     async def test_get_news_multiple_no_auth(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
#         for _ in range(10):
#             await create_random_news(client=client, headers=headers)
#         response = await client.get("/news", headers=None)
#         assert response.status_code == 403
#
#     @pytest.mark.asyncio
#     async def test_get_news(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
#         news = await create_base_news(client=client, headers=headers)
#         response = await client.get(f"/news/{news['guid']}", headers=headers)
#         assert response.status_code == 200
#
#         news = response.json()
#         assert news["name"] == test_models.NEWS_CREATE_NAME
#         assert news["description"] == test_models.NEWS_CREATE_DESCRIPTION
#         assert news["likes"] == 0
#         assert news["media"] == test_models.NEWS_CREATE_MEDIA
#         assert news["categories"] == test_models.NEWS_CREATE_CATEGORIES
#         await self.check_system(news)
#
#     @pytest.mark.asyncio
#     async def test_post_news(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
#         response = await client.post("/news", headers=headers, json=jsonable_encoder(test_models.NEWS_CREATE))
#         assert response.status_code == 201
#
#         news = response.json()
#         assert news["name"] == test_models.NEWS_CREATE_NAME
#         assert news["description"] == test_models.NEWS_CREATE_DESCRIPTION
#         assert news["likes"] == 0
#         assert news["media"] == test_models.NEWS_CREATE_MEDIA
#         assert news["categories"] == test_models.NEWS_CREATE_CATEGORIES
#         await self.check_system(news)
#
#     @pytest.mark.asyncio
#     async def test_put_news(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
#         news = await create_base_news(client=client, headers=headers)
#         response = await client.put(
#             f"/news/{news['guid']}", headers=headers, json=jsonable_encoder(test_models.NEWS_PUT)
#         )
#         assert response.status_code == 200
#
#         news = response.json()
#         assert news["name"] == test_models.NEWS_PUT_NAME
#         assert news["description"] == test_models.NEWS_PUT_DESCRIPTION
#         assert news["likes"] == 0
#         assert news["media"] == test_models.NEWS_PUT_MEDIA
#         assert news["categories"] == test_models.NEWS_PUT_CATEGORIES
#         await self.check_system(news)
#
#     @pytest.mark.asyncio
#     async def test_delete_news(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
#         news = await create_base_news(client=client, headers=headers)
#         response = await client.delete(f"/news/{news['guid']}", headers=headers)
#         assert response.status_code == 204
#
#         response = await client.get(f"/news/{news['guid']}", headers=headers)
#         assert response.status_code == 404
#
#     @pytest.mark.asyncio
#     async def test_patch_news(self, client: AsyncClient, headers, auth_mocker, mocker) -> None:
#         news = await create_base_news(client=client, headers=headers)
#         response = await client.patch(
#             f"/news/{news['guid']}",
#             headers=headers,
#             json=jsonable_encoder(test_models.NEWS_PATCH, exclude_unset=True),
#         )
#         assert response.status_code == 200
#
#         news = response.json()
#         assert news["name"] == test_models.NEWS_PATCH_NAME
#         await self.check_system(news)
