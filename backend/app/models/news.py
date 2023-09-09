from datetime import datetime

from pydantic import UUID4, BaseModel, Field

from app.models.category import CategoryGet
from app.models.comment import CommentGet
from app.models.media import MediaCreate, MediaGet
from app.models.utils import optional


class NewsBase(BaseModel):
    name: str = Field(description="Имя пользователя")
    description: str = Field(description="Фамилия пользователя")


class NewsCreate(NewsBase):
    media: list[MediaCreate] = Field(description="Список медиа-файлов")
    categories: list[UUID4] = Field(description="Список категорий")


class NewsGet(NewsBase):
    guid: UUID4 = Field(description="Уникальный идентификатор пользователя")
    likes: int = Field(description="Количество лайков")
    comments: list[CommentGet] = Field(description="Список комментариев")
    media: list[MediaGet] = Field(description="Список медиа-файлов")
    categories: list[CategoryGet] = Field(description="Список категорий")
    is_deleted: bool = Field(False, description="Активен ли пользователь")
    created_at: datetime = Field(description="Время создания пользователя")
    updated_at: datetime = Field(description="Время последнего обновления пользователя")

    class Config:
        orm_mode = True


@optional
class NewsPatch(NewsCreate):
    pass
