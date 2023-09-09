from typing import List

from fastapi import APIRouter, Depends, Path, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.models import CategoryCreate, CategoryGet, CategoryPatch
from app.services import CategoryService
from app.services.auth import verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


@router.post(
    "/category",
    response_model=CategoryGet,
    response_description="Категория успешно создана",
    status_code=status.HTTP_201_CREATED,
    description="Создать категорию и вернуть её",
    summary="Создание категории",
)
async def create(
    model: CategoryCreate,
    db: AsyncSession = Depends(get_session),
    category_service: CategoryService = Depends(),
):
    return await category_service.create(db=db, model=model)


@router.get(
    "/category",
    response_model=List[CategoryGet],
    response_description="Успешный возврат списка категорий",
    status_code=status.HTTP_200_OK,
    description="Получить все категории",
    summary="Получение всех категорий",
)
async def get_all(
    db: AsyncSession = Depends(get_session),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    category_service: CategoryService = Depends(),
):
    return await category_service.get_all(db=db, limit=limit, offset=offset)


@router.get(
    "/category/{id}",
    response_model=CategoryGet,
    response_description="Успешный возврат категории",
    status_code=status.HTTP_200_OK,
    description="Получить категорию по её id",
    summary="Получение категорию по id",
)
async def get(
    id: UUID4 = Path(None, description="Id категории"),
    db: AsyncSession = Depends(get_session),
    category_service: CategoryService = Depends(),
):
    return await category_service.get(db=db, guid=id)


@router.put(
    "/category/{id}",
    response_model=CategoryGet,
    response_description="Успешное обновление категории",
    status_code=status.HTTP_200_OK,
    description="Изменить категорию по её id (полное обновление модели)",
    summary="Изменение категории по id",
)
async def update(
    model: CategoryCreate,
    id: UUID4 = Path(None, description="Id категории"),
    db: AsyncSession = Depends(get_session),
    category_service: CategoryService = Depends(),
):
    return await category_service.update(db=db, guid=id, model=model)


@router.patch(
    "/category/{id}",
    response_model=CategoryGet,
    response_description="Успешное частичное обновление категории",
    status_code=status.HTTP_200_OK,
    description="Изменить категорию по её id (частисно обновление модели)",
    summary="Изменение категории по id (только указанные поля будут изменены)",
)
async def patch(
    model: CategoryPatch,
    id: UUID4 = Path(None, description="Id категории"),
    db: AsyncSession = Depends(get_session),
    category_service: CategoryService = Depends(),
):
    return await category_service.patch(db=db, guid=id, model=model)


@router.delete(
    "/category/{id}",
    response_description="Успешное удаление категории",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить категорию по её id",
    summary="Удаление категории по id",
)
async def delete(
    id: UUID4 = Path(None, description="Id категории"),
    db: AsyncSession = Depends(get_session),
    category_service: CategoryService = Depends(),
):
    return await category_service.delete(db=db, guid=id)
