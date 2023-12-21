from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.containers import Container
from app.core.user import current_superuser, current_user
from app.models import User
from app.repositories import DonationRepository
from app.schemas.donation import (
    DonationCreateIn,
    DonationCreateOut,
    DonationDB,
)
from app.services.investment_processing import update_investment_information


router = APIRouter(prefix="/donation", tags=["donation"])


@router.get(
    "/",
    dependencies=[Depends(current_superuser)],
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    summary="Список всех пожертвований.",
)
@inject
async def get_all_donations(
    donation_repository: DonationRepository = Depends(
        Provide[Container.donation_repository]
    ),
):
    """Только для суперпользователей. Возвращает список всех пожертвований."""
    return await donation_repository.get_list()


@router.post(
    "/",
    response_model=DonationCreateOut,
    response_model_exclude_none=True,
    summary="Создание пожертвования.",
)
@inject
async def create_donation(
    obj_in: DonationCreateIn,
    user: User = Depends(current_user),
    donation_repository: DonationRepository = Depends(
        Provide[Container.donation_repository]
    ),
):
    """Сделать пожертвование."""
    new_donation = await donation_repository.create(obj_in=obj_in, user=user)
    await update_investment_information()
    await donation_repository.session.refresh(new_donation)
    return new_donation


@router.get(
    "/my",
    response_model=list[DonationCreateOut],
    response_model_exclude_none=True,
    summary="Все пожертвования пользователя.",
)
@inject
async def get_all_user_donations(
    user: User = Depends(current_user),
    donation_repository: DonationRepository = Depends(
        Provide[Container.donation_repository]
    ),
):
    """Список всех пожертвований текущего пользователя."""
    return await donation_repository.get_all_by_user(user)
