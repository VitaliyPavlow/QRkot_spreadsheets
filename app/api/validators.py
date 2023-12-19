from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.containers import Container
from app.core.exceptions import ObjectIsNoneException
from app.models import CharityProject
from app.repositories import CharityProjectRepository


@inject
async def check_project_name_duplicate(
    name: str,
    session: AsyncSession,
    charity_repository: CharityProjectRepository = Depends(
        Provide[Container.charity_repository]
    ),
) -> None:
    if name:
        try:
            project_id = await charity_repository.get_by_attribute(
                attribute_name="name", search_value=name, session=session
            )
            if project_id:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Проект с таким именем уже существует!",
                )
        except ObjectIsNoneException:
            return


@inject
async def check_project_exists(
    id: int,
    session: AsyncSession,
    charity_repository: CharityProjectRepository = Depends(
        Provide[Container.charity_repository]
    ),
) -> CharityProject:
    try:
        return await charity_repository.get_by_attribute(
            attribute_name="id", search_value=id, session=session
        )
    except ObjectIsNoneException:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Проект с таким id не существует!",
        )


async def check_invested_amount_is_empty(project: CharityProject):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


async def check_project_is_not_closed(project: CharityProject):
    if project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


async def check_project_is_not_closed_for_update(project: CharityProject):
    if project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )


async def check_new_amount_greater_then_invested_amount(
    project: CharityProject, new_amount: int
):
    if new_amount and new_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Новая сумма не может быть меньше уже инвестированной.",
        )
