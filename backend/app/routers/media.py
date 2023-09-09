from typing import List

from fastapi import APIRouter, Depends, Path, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.models import MediaCreate, MediaGet, MediaPatch
from app.services import MediaService
from app.services.auth import verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


@router.post(
    "/media",
    response_model=MediaGet,
    response_description="Медиа-файл успешно создан",
    status_code=status.HTTP_201_CREATED,
    description="Создать медиа-файл и вернуть его",
    summary="Создание медиа-файла",
)
async def create(
    model: MediaCreate,
    db: AsyncSession = Depends(get_session),
    media_service: MediaService = Depends(),
):
    return await media_service.create(db=db, model=model)


@router.get(
    "/media",
    response_model=List[MediaGet],
    response_description="Успешный возврат списка медиа-файлов",
    status_code=status.HTTP_200_OK,
    description="Получить все медиа-файлы",
    summary="Получение всех медиа-файлов",
)
async def get_all(
    db: AsyncSession = Depends(get_session),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    media_service: MediaService = Depends(),
):
    return await media_service.get_all(db=db, limit=limit, offset=offset)


@router.get(
    "/media/{id}",
    response_model=MediaGet,
    response_description="Успешный возврат медиа-файла",
    status_code=status.HTTP_200_OK,
    description="Получить медиа-файл по его id",
    summary="Получение медиа-файла по id",
)
async def get(
    id: UUID4 = Path(None, description="Id медиа-файла"),
    db: AsyncSession = Depends(get_session),
    media_service: MediaService = Depends(),
):
    return await media_service.get(db=db, guid=id)


@router.put(
    "/media/{id}",
    response_model=MediaGet,
    response_description="Успешное обновление медиа-файла",
    status_code=status.HTTP_200_OK,
    description="Изменить медиа-файл по его id (полное обновление модели)",
    summary="Изменение медиа-файла по id",
)
async def update(
    model: MediaCreate,
    id: UUID4 = Path(None, description="Id медиа-файла"),
    db: AsyncSession = Depends(get_session),
    media_service: MediaService = Depends(),
):
    return await media_service.update(db=db, guid=id, model=model)


@router.patch(
    "/media/{id}",
    response_model=MediaGet,
    response_description="Успешное частичное обновление медиа-файла",
    status_code=status.HTTP_200_OK,
    description="Изменить медиа-файл по его id (частисно обновление модели)",
    summary="Изменение медиа-файла по id (только указанные поля будут изменены)",
)
async def patch(
    model: MediaPatch,
    id: UUID4 = Path(None, description="Id медиа-файла"),
    db: AsyncSession = Depends(get_session),
    media_service: MediaService = Depends(),
):
    return await media_service.patch(db=db, guid=id, model=model)


@router.delete(
    "/media/{id}",
    response_description="Успешное удаление медиа-файла",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить медиа-файл по его id",
    summary="Удаление медиа-файла по id",
)
async def delete(
    id: UUID4 = Path(None, description="Id медиа-файла"),
    db: AsyncSession = Depends(get_session),
    media_service: MediaService = Depends(),
):
    return await media_service.delete(db=db, guid=id)
