from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import BigInteger, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast, desc

from app.database.tables import Media, News
from app.models import NewsCreate, NewsPatch
from app.repositories.category import CategoryRepository


class NewsRepository:
    @staticmethod
    async def create(db: AsyncSession, model: NewsCreate) -> News:
        news = News(
            name=model.name,
            description=model.description,
        )
        for m in model.media:
            media = Media(link=m.link)
            news.media.append(media)
        for c in model.categories:
            category = await CategoryRepository.get(db, c)
            news.categories.append(category)
        db.add(news)
        await db.commit()
        await db.refresh(news)
        return news

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> List[News]:
        res = await db.execute(
            select(News).order_by(desc(News.created_at)).offset(cast(offset, BigInteger)).limit(limit)
        )
        return res.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> News:
        res = await db.execute(select(News).where(News.guid == guid).limit(1))
        return res.scalar()

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: NewsCreate) -> News:
        news = await NewsRepository.get(db, guid)

        if news is None:
            raise HTTPException(404, "Новость не найдена")

        await db.execute(update(News).where(News.guid == guid).values(**model.dict(exclude_unset=True)))
        await db.commit()
        await db.refresh(news)

        return news

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: NewsPatch) -> News:
        news = await NewsRepository.get(db, guid)

        if news is None:
            raise HTTPException(404, "Новость не найдена")

        if model is None or not model.dict(exclude_unset=True):
            raise HTTPException(400, "Должно быть задано хотя бы одно новое поле модели")

        await db.execute(update(News).where(News.guid == guid).values(**model.dict(exclude_unset=True)))
        await db.commit()
        await db.refresh(news)

        return news

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> None:
        await db.execute(update(News).where(News.guid == guid).values(is_deleted=True))
        await db.commit()

    @staticmethod
    async def like(db: AsyncSession, guid: UUID4) -> News:
        news = await NewsRepository.get(db, guid)

        if news is None:
            raise HTTPException(404, "Новость не найдена")

        await db.execute(update(News).where(News.guid == guid).values(likes=News.likes + 1))
        await db.commit()
        await db.refresh(news)

        return news

    @staticmethod
    async def dislike(db: AsyncSession, guid: UUID4) -> News:
        news = await NewsRepository.get(db, guid)

        if news is None:
            raise HTTPException(404, "Новость не найдена")

        await db.execute(update(News).where(News.guid == guid).values(likes=News.likes - 1))
        await db.commit()
        await db.refresh(news)

        return news
