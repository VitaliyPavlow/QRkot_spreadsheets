from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.containers import Container
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.models import CharityProject
from app.repositories import CharityProjectRepository
from app.schemas.charity_project import CharityProjectDB
from app.services.google_api_servies import GoogleService


router = APIRouter(prefix="/google", tags=["Google"])


@router.get(
    "/",
    response_model=List[CharityProjectDB],
    dependencies=[Depends(current_superuser)],
    summary="Создать гугл-таблицу с проектами.",
)
@inject
async def get_google_table(
    session: AsyncSession = Depends(get_async_session),
    charity_repository: CharityProjectRepository = Depends(
        Provide[Container.charity_repository]
    ),
    google_service: GoogleService = Depends(Provide[Container.google_service]),
) -> List[CharityProject]:
    """Создать таблицу с отсортированными по срокам сбора проектами."""
    sorted_projects = await charity_repository.get_by_completion_rate(session)
    spreadsheetid = await google_service.spreadsheets_create()
    await google_service.set_user_permissions(spreadsheetid=spreadsheetid)
    await google_service.spreadsheets_update_value(
        spreadsheetid=spreadsheetid, projects=sorted_projects
    )
    return sorted_projects
