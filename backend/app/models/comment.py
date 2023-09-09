from datetime import datetime

from pydantic import UUID4, BaseModel, Field

from app.models.utils import optional


class CommentBase(BaseModel):
    text: str = Field(description="Текст комментария")


class CommentCreate(CommentBase):
    pass


class CommentGet(CommentBase):
    guid: UUID4 = Field(description="Уникальный идентификатор комментария")
    is_deleted: bool = Field(False, description="Удален ли комментарий")
    created_at: datetime = Field(description="Время создания комментария")
    updated_at: datetime = Field(description="Время последнего обновления комментария")

    class Config:
        orm_mode = True


@optional
class CommentPatch(CommentCreate):
    pass
