from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import BigInteger, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import Media
from app.models import MediaCreate, MediaPatch


class MediaRepository:
    @staticmethod
    async def create(db: AsyncSession, model: MediaCreate) -> Media:
        media = Media(**model.dict(exclude_unset=True))
        db.add(media)
        await db.commit()
        await db.refresh(media)
        return media

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> List[Media]:
        res = await db.execute(select(Media).offset(cast(offset, BigInteger)).limit(limit))
        return res.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> Media:
        res = await db.execute(select(Media).where(Media.guid == guid).limit(1))
        return res.scalar()

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: MediaCreate) -> Media:
        media = await MediaRepository.get(db, guid)

        if media is None:
            raise HTTPException(404, "Медиа-файл не найден")

        await db.execute(update(Media).where(Media.guid == guid).values(**model.dict(exclude_unset=True)))
        await db.commit()
        await db.refresh(media)

        return media

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: MediaPatch) -> Media:
        media = await MediaRepository.get(db, guid)

        if media is None:
            raise HTTPException(404, "Медиа-файл не найден")

        if model is None or not model.dict(exclude_unset=True):
            raise HTTPException(400, "Должно быть задано хотя бы одно новое поле модели")

        await db.execute(update(Media).where(Media.guid == guid).values(**model.dict(exclude_unset=True)))
        await db.commit()
        await db.refresh(media)

        return media

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> None:
        await db.execute(update(Media).where(Media.guid == guid).values(is_deleted=True))
        await db.commit()
