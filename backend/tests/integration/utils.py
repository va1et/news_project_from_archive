import secrets

from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

import tests.models as test_models


async def create_base_comment(client: AsyncClient, headers: dict) -> dict:
    response = await client.post("/comment", headers=headers, json=jsonable_encoder(test_models.COMMENT_CREATE))
    return response.json()


async def create_random_comment(client: AsyncClient, headers: dict) -> dict:
    text = secrets.token_hex(10)

    body = {
        "text": text,
    }

    response = await client.post("/comment", headers=headers, json=jsonable_encoder(body))
    return response.json()


async def create_base_category(client: AsyncClient, headers: dict) -> dict:
    response = await client.post("/category", headers=headers, json=jsonable_encoder(test_models.CATEGORY_CREATE))
    return response.json()


async def create_random_category(client: AsyncClient, headers: dict) -> dict:
    name = secrets.token_hex(10)

    body = {
        "name": name,
    }

    response = await client.post("/category", headers=headers, json=jsonable_encoder(body))
    return response.json()


async def create_base_media(client: AsyncClient, headers: dict) -> dict:
    response = await client.post("/media", headers=headers, json=jsonable_encoder(test_models.MEDIA_CREATE))
    return response.json()


async def create_random_media(client: AsyncClient, headers: dict) -> dict:
    link = f"https://{secrets.token_hex(10)}.com"

    body = {
        "link": link,
    }

    response = await client.post("/media", headers=headers, json=jsonable_encoder(body))
    return response.json()


async def create_base_user(client: AsyncClient, headers: dict) -> dict:
    response = await client.post("/user", headers=headers, json=jsonable_encoder(test_models.USER_CREATE))
    return response.json()


async def create_random_user(client: AsyncClient, headers: dict) -> dict:
    email = secrets.token_hex(10) + "@test.com"
    first_name = secrets.token_hex(10)
    last_name = secrets.token_hex(10)
    middle_name = secrets.token_hex(10)
    role = "admin"
    password = secrets.token_hex(10)

    body = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "role": role,
        "password": password,
    }

    response = await client.post("/user", headers=headers, json=jsonable_encoder(body))
    return response.json()


async def create_base_news(client: AsyncClient, headers: dict) -> dict:
    response = await client.post("/news", headers=headers, json=jsonable_encoder(test_models.NEWS_CREATE))
    return response.json()


async def create_random_news(client: AsyncClient, headers: dict) -> dict:
    name = secrets.token_hex(10)
    description = secrets.token_hex(10)
    media = jsonable_encoder(test_models.MEDIA_CREATE)
    categories = jsonable_encoder(test_models.CATEGORY_CREATE)

    body = {
        "name": name,
        "description": description,
        "media": [media],
        "categories": [categories],
    }

    response = await client.post("/user", headers=headers, json=jsonable_encoder(body))
    return response.json()
