import contextlib
from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException

from app.containers import Container
from app.core.exceptions import ObjectIsNoneException
from app.models import CharityProject
from app.repositories import CharityProjectRepository


@inject
async def check_project_name_duplicate(
    name: str,
    charity_repository: CharityProjectRepository = Depends(
        Provide[Container.charity_repository]
    ),
) -> None:
    """Проверить уникальность имени проекта."""
    with contextlib.suppress(ObjectIsNoneException):
        project_id = await charity_repository.get_by_attribute(
            attribute_name="name", search_value=name
        )
        if project_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Проект с таким именем уже существует!",
            )


async def check_invested_amount_is_empty(project: CharityProject):
    """Проверить, что параметр invested_amount не пустой."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


async def check_project_is_not_closed(project: CharityProject):
    """Проверить, что проект открыт."""
    if project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


async def check_project_is_not_closed_for_update(project: CharityProject):
    """Проверить, что проект открыт для обновления."""
    if project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )


async def check_new_amount_greater_then_invested_amount(
    project: CharityProject, new_amount: int
):
    """Проверить, что новая сумма больше уже инвестированной."""
    if new_amount and new_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Новая сумма не может быть меньше уже инвестированной.",
        )
