from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import BigInteger, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import Category
from app.models import CategoryCreate, CategoryPatch


class CategoryRepository:
    @staticmethod
    async def create(db: AsyncSession, model: CategoryCreate) -> Category:
        category = Category(**model.dict(exclude_unset=True))
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> List[Category]:
        res = await db.execute(select(Category).offset(cast(offset, BigInteger)).limit(limit))
        return res.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> Category:
        res = await db.execute(select(Category).where(Category.guid == guid).limit(1))
        return res.scalar()

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> Category:
        res = await db.execute(select(Category).where(Category.name == name).limit(1))
        return res.scalar()

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: CategoryCreate) -> Category:
        category = await CategoryRepository.get(db, guid)

        if category is None:
            raise HTTPException(404, "Категория не найдена")

        await db.execute(update(Category).where(Category.guid == guid).values(**model.dict(exclude_unset=True)))
        await db.commit()
        await db.refresh(category)

        return category

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: CategoryPatch) -> Category:
        category = await CategoryRepository.get(db, guid)

        if category is None:
            raise HTTPException(404, "Категория не найдена")

        if model is None or not model.dict(exclude_unset=True):
            raise HTTPException(400, "Должно быть задано хотя бы одно новое поле модели")

        await db.execute(update(Category).where(Category.guid == guid).values(**model.dict(exclude_unset=True)))
        await db.commit()
        await db.refresh(category)

        return category

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> None:
        await db.execute(update(Category).where(Category.guid == guid).values(is_deleted=True))
        await db.commit()
