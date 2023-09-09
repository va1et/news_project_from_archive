from __future__ import annotations

import feedparser
from fastapi import HTTPException, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CategoryCreate, MediaCreate, NewsCreate, NewsGet, NewsPatch
from app.repositories import CategoryRepository, NewsRepository


class NewsService:
    @staticmethod
    async def create(db: AsyncSession, model: NewsCreate) -> NewsGet:
        news = await NewsRepository.create(db, model)
        return NewsGet.from_orm(news)

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[NewsGet]:
        news = await NewsRepository.get_all(db, offset=offset, limit=limit)
        if news is None:
            raise HTTPException(404, "Новости не найдены")
        return [NewsGet.from_orm(n) for n in news]

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> NewsGet:
        news = await NewsRepository.get(db, guid)
        if news is None:
            raise HTTPException(404, "Новость не найдена")
        return NewsGet.from_orm(news)

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: NewsCreate) -> NewsGet:
        news = await NewsRepository.update(db, guid, model)
        if news is None:
            raise HTTPException(404, "Новость не найдена")
        return NewsGet.from_orm(news)

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: NewsPatch) -> NewsGet:
        news = await NewsRepository.patch(db, guid, model)
        if news is None:
            raise HTTPException(404, "Новость не найдена")
        return NewsGet.from_orm(news)

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> Response(status_code=204):
        await NewsRepository.delete(db, guid)
        return Response(status_code=204)

    @staticmethod
    async def like(db: AsyncSession, guid: UUID4) -> NewsGet:
        news = await NewsRepository.like(db, guid)
        if news is None:
            raise HTTPException(404, "Новость не найдена")
        return NewsGet.from_orm(news)

    @staticmethod
    async def dislike(db: AsyncSession, guid: UUID4) -> NewsGet:
        news = await NewsRepository.dislike(db, guid)
        if news is None:
            raise HTTPException(404, "Новость не найдена")
        return NewsGet.from_orm(news)

    @staticmethod
    async def parse(db: AsyncSession) -> Response(status_code=204):
        rbc_url = "http://static.feed.rbc.ru/rbc/logical/footer/news.rss"
        lenta_url = "https://lenta.ru/rss/news"
        placeholder = "https://www.unfe.org/wp-content/uploads/2019/04/SM-placeholder.png"
        feed = feedparser.parse(rbc_url)
        for item in feed["items"]:
            category = await CategoryRepository.get_by_name(db, item["category"])
            if category is None:
                category = await CategoryRepository.create(db, CategoryCreate(name=item["category"]))
            await NewsRepository.create(
                db,
                NewsCreate(
                    name=item["title"],
                    description=item["description"],
                    media=[
                        MediaCreate(link=item["rbc_news_url"] if "rbc_news_url" in item else placeholder),
                        MediaCreate(link=placeholder),
                    ],
                    categories=[category.guid],
                ),
            )
        feed = feedparser.parse(lenta_url)
        for item in feed["items"]:
            category = await CategoryRepository.get_by_name(db, item["category"])
            if category is None:
                category = await CategoryRepository.create(db, CategoryCreate(name=item["tags"][0]["term"]))

            media_link = placeholder
            for link in item["links"]:
                if link["rel"] == "enclosure":
                    media_link = link["href"]
                    break

            await NewsRepository.create(
                db,
                NewsCreate(
                    name=item["title"],
                    description=item["summary"],
                    media=[
                        MediaCreate(link=media_link),
                        MediaCreate(link=placeholder),
                    ],
                    categories=[category.guid],
                ),
            )
        return Response(status_code=204)
