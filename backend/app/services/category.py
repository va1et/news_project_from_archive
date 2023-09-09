from __future__ import annotations

from fastapi import HTTPException, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CategoryCreate, CategoryGet, CategoryPatch
from app.repositories import CategoryRepository


class CategoryService:
    @staticmethod
    async def create(db: AsyncSession, model: CategoryCreate) -> CategoryGet:
        category = await CategoryRepository.create(db, model)
        if category is None:
            raise HTTPException(409, "Категория с таким названием уже существует")
        return CategoryGet.from_orm(category)

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[CategoryGet]:
        categories = await CategoryRepository.get_all(db, offset=offset, limit=limit)
        if categories is None:
            raise HTTPException(404, "Категории не найдены")
        return [CategoryGet.from_orm(c) for c in categories]

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> CategoryGet:
        category = await CategoryRepository.get(db, guid)
        if category is None:
            raise HTTPException(404, "Категория не найдена")
        return CategoryGet.from_orm(category)

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: CategoryCreate) -> CategoryGet:
        category = await CategoryRepository.update(db, guid, model)
        if category is None:
            raise HTTPException(404, "Категория не найдена")
        return CategoryGet.from_orm(category)

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: CategoryPatch) -> CategoryGet:
        category = await CategoryRepository.patch(db, guid, model)
        if category is None:
            raise HTTPException(404, "Категория не найдена")
        return CategoryGet.from_orm(category)

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> Response(status_code=204):
        await CategoryRepository.delete(db, guid)
        return Response(status_code=204)
