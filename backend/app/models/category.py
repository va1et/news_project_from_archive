from datetime import datetime

from pydantic import UUID4, BaseModel, Field

from app.models.utils import optional


class CategoryBase(BaseModel):
    name: str = Field(description="Название категории")


class CategoryCreate(CategoryBase):
    pass


class CategoryGet(CategoryBase):
    guid: UUID4 = Field(description="Уникальный идентификатор категории")
    is_deleted: bool = Field(False, description="Удалена ли категория")
    created_at: datetime = Field(description="Время создания категории")
    updated_at: datetime = Field(description="Время последнего обновления категории")

    class Config:
        orm_mode = True


@optional
class CategoryPatch(CategoryCreate):
    pass
