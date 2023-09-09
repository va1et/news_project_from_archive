from __future__ import annotations

from fastapi import HTTPException, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CommentCreate, CommentGet, CommentPatch
from app.repositories import CommentRepository


class CommentService:
    @staticmethod
    async def create(db: AsyncSession, model: CommentCreate) -> CommentGet:
        comment = await CommentRepository.create(db, model)
        return CommentGet.from_orm(comment)

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[CommentGet]:
        comments = await CommentRepository.get_all(db, offset=offset, limit=limit)
        if comments is None:
            raise HTTPException(404, "Комментарии не найдены")
        return [CommentGet.from_orm(c) for c in comments]

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> CommentGet:
        comment = await CommentRepository.get(db, guid)
        if comment is None:
            raise HTTPException(404, "Комментарий не найден")
        return CommentGet.from_orm(comment)

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: CommentCreate) -> CommentGet:
        comment = await CommentRepository.update(db, guid, model)
        if comment is None:
            raise HTTPException(404, "Комментарий не найден")
        return CommentGet.from_orm(comment)

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: CommentPatch) -> CommentGet:
        comment = await CommentRepository.patch(db, guid, model)
        if comment is None:
            raise HTTPException(404, "Комментарий не найден")
        return CommentGet.from_orm(comment)

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> Response(status_code=204):
        await CommentRepository.delete(db, guid)
        return Response(status_code=204)
