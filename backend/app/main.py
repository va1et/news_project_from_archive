from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import config
from app.models.exceptions import add_exception_handlers, catch_unhandled_exceptions
from app.routers.auth import router as auth_router
from app.routers.category import router as category_router
from app.routers.comment import router as comment_router
from app.routers.media import router as media_router
from app.routers.news import router as news_router
from app.routers.user import router as user_router

tags_metadata = [
    {"name": "auth", "description": "Авторизация"},
    {"name": "users", "description": "Работа с пользователями"},
    {"name": "news", "description": "Работа с новостями"},
    {"name": "categories", "description": "Работа с категориями"},
    {"name": "media", "description": "Работа с медиа-файлами"},
    {"name": "comments", "description": "Работа с комментариями"},
]

app = FastAPI(
    debug=config.DEBUG,
    openapi_tags=tags_metadata,
    openapi_url=f"{config.BACKEND_PREFIX}/openapi.json",
    title=config.BACKEND_TTILE,
    description=config.BACKEND_DESCRIPTION,
)

app.middleware("http")(catch_unhandled_exceptions)
add_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, tags=["users"])
app.include_router(news_router, tags=["news"])
app.include_router(category_router, tags=["categories"])
app.include_router(media_router, tags=["media"])
app.include_router(comment_router, tags=["comments"])
