from datetime import datetime

from pydantic import UUID4, BaseModel, Field, HttpUrl

from app.models.utils import optional


class MediaBase(BaseModel):
    link: HttpUrl = Field(description="Ссылка на медиа-файл")


class MediaCreate(MediaBase):
    pass


class MediaGet(MediaBase):
    guid: UUID4 = Field(description="Уникальный идентификатор медиа-файла")
    is_deleted: bool = Field(False, description="Удален ли медиа-файл")
    created_at: datetime = Field(description="Время создания медиа-файла")
    updated_at: datetime = Field(description="Время последнего обновления медиа-файла")

    class Config:
        orm_mode = True


@optional
class MediaPatch(MediaCreate):
    pass
