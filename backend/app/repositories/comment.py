from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import BigInteger, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import Comment
from app.models import CommentCreate, CommentPatch


class CommentRepository:
    @staticmethod
    async def create(db: AsyncSession, model: CommentCreate) -> Comment:
        comment = Comment(**model.dict(exclude_unset=True))
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> List[Comment]:
        res = await db.execute(select(Comment).offset(cast(offset, BigInteger)).limit(limit))
        return res.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> Comment:
        res = await db.execute(select(Comment).where(Comment.guid == guid).limit(1))
        return res.scalar()

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: CommentCreate) -> Comment:
        comment = await CommentRepository.get(db, guid)

        if comment is None:
            raise HTTPException(404, "Комментарий не найден")

        await db.execute(update(Comment).where(Comment.guid == guid).values(**model.dict(exclude_unset=True)))
        await db.commit()
        await db.refresh(comment)

        return comment

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: CommentPatch) -> Comment:
        comment = await CommentRepository.get(db, guid)

        if comment is None:
            raise HTTPException(404, "Комментарий не найден")

        if model is None or not model.dict(exclude_unset=True):
            raise HTTPException(400, "Должно быть задано хотя бы одно новое поле модели")

        await db.execute(update(Comment).where(Comment.guid == guid).values(**model.dict(exclude_unset=True)))
        await db.commit()
        await db.refresh(comment)

        return comment

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> None:
        await db.execute(update(Comment).where(Comment.guid == guid).values(is_deleted=True))
        await db.commit()
