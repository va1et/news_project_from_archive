from __future__ import annotations

from fastapi import HTTPException, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MediaCreate, MediaGet, MediaPatch
from app.repositories import MediaRepository


class MediaService:
    @staticmethod
    async def create(db: AsyncSession, model: MediaCreate) -> MediaGet:
        media = await MediaRepository.create(db, model)
        return MediaGet.from_orm(media)

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[MediaGet]:
        media = await MediaRepository.get_all(db, offset=offset, limit=limit)
        if media is None:
            raise HTTPException(404, "Медиа-файлы не найдены")
        return [MediaGet.from_orm(m) for m in media]

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> MediaGet:
        media = await MediaRepository.get(db, guid)
        if media is None:
            raise HTTPException(404, "Медиа-файл не найден")
        return MediaGet.from_orm(media)

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: MediaCreate) -> MediaGet:
        media = await MediaRepository.update(db, guid, model)
        if media is None:
            raise HTTPException(404, "Медиа-файл не найден")
        return MediaGet.from_orm(media)

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: MediaPatch) -> MediaGet:
        media = await MediaRepository.patch(db, guid, model)
        if media is None:
            raise HTTPException(404, "Медиа-файл не найден")
        return MediaGet.from_orm(media)

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> Response(status_code=204):
        await MediaRepository.delete(db, guid)
        return Response(status_code=204)
