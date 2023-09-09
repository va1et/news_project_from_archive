from typing import List

from fastapi import APIRouter, Depends, Path, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.models import NewsCreate, NewsGet, NewsPatch
from app.services import NewsService
from app.services.auth import verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


@router.post(
    "/news",
    response_model=NewsGet,
    response_description="Новость успешно создана",
    status_code=status.HTTP_201_CREATED,
    description="Создать новость и вернуть её",
    summary="Создание новости",
)
async def create(
    model: NewsCreate,
    db: AsyncSession = Depends(get_session),
    news_service: NewsService = Depends(),
):
    return await news_service.create(db=db, model=model)


@router.get(
    "/news",
    response_model=List[NewsGet],
    response_description="Успешный возврат списка новостей",
    status_code=status.HTTP_200_OK,
    description="Получить все новости",
    summary="Получение всех новостей",
)
async def get_all(
    db: AsyncSession = Depends(get_session),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    news_service: NewsService = Depends(),
):
    return await news_service.get_all(db=db, limit=limit, offset=offset)


@router.get(
    "/news/{id}",
    response_model=NewsGet,
    response_description="Успешный возврат новости",
    status_code=status.HTTP_200_OK,
    description="Получить новость по её id",
    summary="Получение новости по id",
)
async def get(
    id: UUID4 = Path(None, description="Id новости"),
    db: AsyncSession = Depends(get_session),
    news_service: NewsService = Depends(),
):
    return await news_service.get(db=db, guid=id)


@router.put(
    "/news/{id}",
    response_model=NewsGet,
    response_description="Успешное обновление новости",
    status_code=status.HTTP_200_OK,
    description="Изменить новость по её id (полное обновление модели)",
    summary="Изменение новости по id",
)
async def update(
    model: NewsCreate,
    id: UUID4 = Path(None, description="Id новости"),
    db: AsyncSession = Depends(get_session),
    news_service: NewsService = Depends(),
):
    return await news_service.update(db=db, guid=id, model=model)


@router.patch(
    "/news/{id}",
    response_model=NewsGet,
    response_description="Успешное частичное обновление новости",
    status_code=status.HTTP_200_OK,
    description="Изменить новость по её id (частисно обновление модели)",
    summary="Изменение новости по id (только указанные поля будут изменены)",
)
async def patch(
    model: NewsPatch,
    id: UUID4 = Path(None, description="Id новости"),
    db: AsyncSession = Depends(get_session),
    news_service: NewsService = Depends(),
):
    return await news_service.patch(db=db, guid=id, model=model)


@router.delete(
    "/news/{id}",
    response_description="Успешное удаление новости",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить новость по её id",
    summary="Удаление новости по id",
)
async def delete(
    id: UUID4 = Path(None, description="Id новости"),
    db: AsyncSession = Depends(get_session),
    news_service: NewsService = Depends(),
):
    return await news_service.delete(db=db, guid=id)


@router.post(
    "/news/like/{id}",
    response_model=NewsGet,
    response_description="Успешное обновление новости",
    status_code=status.HTTP_200_OK,
    description="Лайкнуть новость по её id",
    summary="Лайк новости по id",
)
async def like(
    id: UUID4 = Path(None, description="Id новости"),
    db: AsyncSession = Depends(get_session),
    news_service: NewsService = Depends(),
):
    return await news_service.like(db=db, guid=id)


@router.post(
    "/news/dislike/{id}",
    response_model=NewsGet,
    response_description="Успешное обновление новости",
    status_code=status.HTTP_200_OK,
    description="Дизлайкнуть новость по её id",
    summary="Дизлайк новости по id",
)
async def dislike(
    id: UUID4 = Path(None, description="Id новости"),
    db: AsyncSession = Depends(get_session),
    news_service: NewsService = Depends(),
):
    return await news_service.dislike(db=db, guid=id)


@router.post(
    "/news/parse",
    response_description="Успешный парсинг новостей",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Спарсить новости",
    summary="Парсинг новостей",
)
async def parse(
    db: AsyncSession = Depends(get_session),
    news_service: NewsService = Depends(),
):
    return await news_service.parse(db=db)
