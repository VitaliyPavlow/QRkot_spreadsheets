from datetime import datetime
from typing import Union

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.containers import Container
from app.models import CharityProject, Donation
from app.repositories import CharityProjectRepository, DonationRepository


async def close_the_object(
    obj: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """Присвоить объекту атрибуты закрытого и текущие дату/время."""
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()
    return obj


@inject
async def update_investment_information(
    session: AsyncSession,
    charity_repository: CharityProjectRepository = Depends(
        Provide[Container.charity_repository]
    ),
    donation_repository: DonationRepository = Depends(
        Provide[Container.donation_repository]
    ),
) -> None:
    """
    Обновить информацию об инвестициях в открытых проектах и пожертвованиях.
    Успешно потраченные/инвестированные закрыть.
    Посчитать разницу и сохранить остатки.
    """
    open_projects = await charity_repository.get_all_open_objects_sorted_by_id(
        session
    )
    open_donations = (
        await donation_repository.get_all_open_objects_sorted_by_id(session)
    )

    for donation in open_donations:
        donation.invested_amount = donation.invested_amount or 0
        donation_sum = donation.full_amount - donation.invested_amount
        for project in open_projects:
            investment = project.invested_amount + donation_sum
            tail = project.full_amount - investment
            if tail > 0:
                project.invested_amount = investment
                donation = await close_the_object(donation)
                session.add(project)
                break
            elif tail < 0:
                donation.invested_amount += (
                    project.full_amount - project.invested_amount
                )
                project = await close_the_object(project)
                donation_sum = abs(tail)
                session.add(project)
            else:
                project = await close_the_object(project)
                donation = await close_the_object(donation)
                session.add(project)
                break
        session.add(donation)
    await session.commit()
