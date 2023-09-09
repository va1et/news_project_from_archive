from pydantic import UUID4

from app.models import (
    CategoryCreate,
    CategoryPatch,
    CommentCreate,
    CommentPatch,
    MediaCreate,
    MediaPatch,
    NewsCreate,
    NewsPatch,
    UserCreate,
    UserPatch,
)

USER_CREATE_SUB = "00000000-33b6-4b04-9dfb-b809a8561a4b"

COMMENT_CREATE_TEXT = "test"
COMMENT_CREATE = CommentCreate(
    text=COMMENT_CREATE_TEXT,
)

COMMENT_PUT_TEXT = "put"
COMMENT_PUT = CommentCreate(
    text=COMMENT_PUT_TEXT,
)

COMMENT_PATCH_TEXT = "patch"
COMMENT_PATCH = CommentPatch(
    text=COMMENT_PATCH_TEXT,
)

CATEGORY_CREATE_NAME = "test"
CATEGORY_CREATE = CategoryCreate(
    name=CATEGORY_CREATE_NAME,
)

CATEGORY_PUT_NAME = "put"
CATEGORY_PUT = CategoryCreate(
    name=CATEGORY_PUT_NAME,
)

CATEGORY_PATCH_NAME = "patch"
CATEGORY_PATCH = CategoryPatch(
    name=CATEGORY_PATCH_NAME,
)

MEDIA_CREATE_LINK = "https://create.com"
MEDIA_CREATE = MediaCreate(
    link=MEDIA_CREATE_LINK,
)

MEDIA_PUT_LINK = "https://put.com"
MEDIA_PUT = MediaCreate(
    link=MEDIA_PUT_LINK,
)

MEDIA_PATCH_LINK = "https://patch.com"
MEDIA_PATCH = MediaPatch(
    link=MEDIA_PATCH_LINK,
)

USER_CREATE_EMAIL = "student@test.com"
USER_CREATE_FIRST_NAME = "test"
USER_CREATE_LAST_NAME = "test"
USER_CREATE_MIDDLE_NAME = "test"
USER_CREATE_ROLE = "student"
USER_CREATE_PASSWORD = "test"
USER_CREATE = UserCreate(
    email=USER_CREATE_EMAIL,
    first_name=USER_CREATE_FIRST_NAME,
    last_name=USER_CREATE_LAST_NAME,
    middle_name=USER_CREATE_MIDDLE_NAME,
    role=USER_CREATE_ROLE,
    password=USER_CREATE_PASSWORD,
)

USER_PUT_EMAIL = "put@test.com"
USER_PUT_FIRST_NAME = "put"
USER_PUT_LAST_NAME = "put"
USER_PUT_MIDDLE_NAME = "put"
USER_PUT_ROLE = "admin"
USER_PUT_PASSWORD = "put"
USER_PUT = UserCreate(
    email=USER_PUT_EMAIL,
    first_name=USER_PUT_FIRST_NAME,
    last_name=USER_PUT_LAST_NAME,
    middle_name=USER_PUT_MIDDLE_NAME,
    role=USER_PUT_ROLE,
    password=USER_PUT_PASSWORD,
)

USER_PATCH_EMAIL = "patch@test.com"
USER_PATCH = UserPatch(
    email=USER_PATCH_EMAIL,
)

NEWS_CREATE_NAME = "test"
NEWS_CREATE_DESCRIPTION = "test"
NEWS_CREATE_MEDIA = MEDIA_CREATE.copy()
NEWS_CREATE_CATEGORIES = [UUID4("4770f582-6419-417d-9908-4277fd03941e")]
NEWS_CREATE = NewsCreate(
    name=NEWS_CREATE_NAME,
    description=NEWS_CREATE_DESCRIPTION,
    media=[NEWS_CREATE_MEDIA],
    categories=NEWS_CREATE_CATEGORIES,
)

NEWS_PUT_NAME = "put"
NEWS_PUT_DESCRIPTION = "put"
NEWS_PUT_MEDIA = MEDIA_CREATE.copy()
NEWS_PUT_CATEGORIES = [UUID4("4770f583-6419-417d-9908-4277fd03941e")]
NEWS_PUT = NewsCreate(
    name=NEWS_PUT_NAME,
    description=NEWS_PUT_DESCRIPTION,
    media=[NEWS_PUT_MEDIA],
    categories=NEWS_PUT_CATEGORIES,
)

NEWS_PATCH_NAME = "patch"
NEWS_PATCH = NewsPatch(
    name=NEWS_PATCH_NAME,
)
