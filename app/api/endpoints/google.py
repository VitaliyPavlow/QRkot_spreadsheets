from typing import List

from aiogoogle import Aiogoogle
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.containers import Container
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.repositories import CharityProjectRepository
from app.schemas.charity_project import CharityProjectDB
from app.services.google_api_servies import GoogleServices
from app.models import CharityProject


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
    wrapper_services: Aiogoogle = Depends(get_service),
    google_services: GoogleServices = Depends(Provide[Container.google_services])
) -> List[CharityProject]:
    """Создать таблицу с отсортированными по срокам сбора проектами."""
    sorted_projects = await charity_repository.get_projects_by_completion_rate(
        session
    )
    spreadsheetid = await google_services.spreadsheets_create(wrapper_services=wrapper_services)
    await google_services.set_user_permissions(spreadsheetid=spreadsheetid, wrapper_services=wrapper_services)
    await google_services.spreadsheets_update_value(
        spreadsheetid=spreadsheetid, projects=sorted_projects, wrapper_services=wrapper_services
    )
    return sorted_projects
