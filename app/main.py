from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.containers import Container
from app.core.init_db import create_first_superuser


def create_app() -> FastAPI:
    """Фабрика FastAPI."""
    container = Container()
    app = FastAPI(
        title=settings.app_title,
        description=settings.description,
    )
    app.container = container

    @app.on_event("startup")
    async def startup():
        await create_first_superuser()

    app.include_router(router=main_router)
    return app


app = create_app()
