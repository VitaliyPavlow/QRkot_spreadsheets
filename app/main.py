from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.routers import main_router
from app.containers import Container
from app.core.config import settings
from app.core.exceptions import ObjectIsNoneException
from app.core.init_db import create_first_superuser


def create_app() -> FastAPI:
    """Фабрика FastAPI."""
    container = Container()
    app = FastAPI(
        title=settings.app_title,
        description=settings.description,
    )
    app.container = container

    @app.exception_handler(ObjectIsNoneException)
    async def object_is_none_exception_handler(request, exc):
        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content={"detail": "Проект с таким id не существует!"},
        )

    @app.on_event("startup")
    async def startup():
        await create_first_superuser()

    app.include_router(router=main_router)
    return app


app = create_app()
