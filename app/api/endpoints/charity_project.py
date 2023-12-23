from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.api.validators import (
    check_invested_amount_is_empty,
    check_new_amount_greater_then_invested_amount,
    check_project_is_not_closed,
    check_project_is_not_closed_for_update,
    check_project_name_duplicate,
)
from app.containers import Container
from app.core.user import current_superuser
from app.repositories import CharityProjectRepository
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment_processing import update_investment_information


router = APIRouter(prefix="/charity_project", tags=["charity project"])


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    summary="Получить все проекты для сбора пожертвований.",
)
@inject
async def get_all_charity_projects(
    charity_repository: CharityProjectRepository = Depends(
        Provide[Container.charity_repository]
    ),
):
    """Получить список всех проектов."""
    return await charity_repository.get_list()


@router.post(
    "/",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
    summary="Создать новый попрошайнический проект.",
)
@inject
async def create_new_charity_project(
    charity: CharityProjectCreate,
    charity_repository: CharityProjectRepository = Depends(
        Provide[Container.charity_repository]
    ),
):
    """Создать новый проект."""
    await check_project_name_duplicate(charity.name)
    new_project = await charity_repository.create(charity)
    await update_investment_information()
    await charity_repository.refresh(new_project)
    return new_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary="Удали проект к чертям кошачьим жадный жадина!",
)
@inject
async def delete_charity_project(
    project_id: int,
    charity_repository: CharityProjectRepository = Depends(
        Provide[Container.charity_repository]
    ),
):
    """Удаление проекта. Только для суперюзеров. Только пустые проекты."""
    project = await charity_repository.get_by_attribute("id", project_id)
    await check_project_is_not_closed(project)
    await check_invested_amount_is_empty(project)
    return await charity_repository.remove(project)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary="Обнови проект, плюсани пару рыбок котикам.",
)
@inject
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    charity_repository: CharityProjectRepository = Depends(
        Provide[Container.charity_repository]
    ),
):
    """Редактирование проекта. Только открытй проект. Только суперюзер."""
    project = await charity_repository.get_by_attribute("id", project_id)
    await check_project_is_not_closed_for_update(project)
    await check_project_name_duplicate(obj_in.name)
    await check_new_amount_greater_then_invested_amount(
        project, obj_in.full_amount
    )
    return await charity_repository.update(project, obj_in)
