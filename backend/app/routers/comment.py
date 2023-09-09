from typing import List

from fastapi import APIRouter, Depends, Path, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.models import CommentCreate, CommentGet, CommentPatch
from app.services import CommentService
from app.services.auth import verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


@router.post(
    "/comment",
    response_model=CommentGet,
    response_description="Комментарий успешно создан",
    status_code=status.HTTP_201_CREATED,
    description="Создать комментарий и вернуть его",
    summary="Создание комментария",
)
async def create(
    model: CommentCreate,
    db: AsyncSession = Depends(get_session),
    comment_service: CommentService = Depends(),
):
    return await comment_service.create(db=db, model=model)


@router.get(
    "/comment",
    response_model=List[CommentGet],
    response_description="Успешный возврат списка комментариев",
    status_code=status.HTTP_200_OK,
    description="Получить все комментарии",
    summary="Получение всех комментариев",
)
async def get_all(
    db: AsyncSession = Depends(get_session),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    comment_service: CommentService = Depends(),
):
    return await comment_service.get_all(db=db, limit=limit, offset=offset)


@router.get(
    "/comment/{id}",
    response_model=CommentGet,
    response_description="Успешный возврат комментария",
    status_code=status.HTTP_200_OK,
    description="Получить комментарий по его id",
    summary="Получение комментария по id",
)
async def get(
    id: UUID4 = Path(None, description="Id комментария"),
    db: AsyncSession = Depends(get_session),
    comment_service: CommentService = Depends(),
):
    return await comment_service.get(db=db, guid=id)


@router.put(
    "/comment/{id}",
    response_model=CommentGet,
    response_description="Успешное обновление комментария",
    status_code=status.HTTP_200_OK,
    description="Изменить комментарий по его id (полное обновление модели)",
    summary="Изменение комментария по id",
)
async def update(
    model: CommentCreate,
    id: UUID4 = Path(None, description="Id комментария"),
    db: AsyncSession = Depends(get_session),
    comment_service: CommentService = Depends(),
):
    return await comment_service.update(db=db, guid=id, model=model)


@router.patch(
    "/comment/{id}",
    response_model=CommentGet,
    response_description="Успешное частичное обновление комментария",
    status_code=status.HTTP_200_OK,
    description="Изменить комментарий по его id (частисно обновление модели)",
    summary="Изменение комментария по id (только указанные поля будут изменены)",
)
async def patch(
    model: CommentPatch,
    id: UUID4 = Path(None, description="Id комментария"),
    db: AsyncSession = Depends(get_session),
    comment_service: CommentService = Depends(),
):
    return await comment_service.patch(db=db, guid=id, model=model)


@router.delete(
    "/comment/{id}",
    response_description="Успешное удаление комментария",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить комментарий по его id",
    summary="Удаление комментария по id",
)
async def delete(
    id: UUID4 = Path(None, description="Id комментария"),
    db: AsyncSession = Depends(get_session),
    comment_service: CommentService = Depends(),
):
    return await comment_service.delete(db=db, guid=id)
