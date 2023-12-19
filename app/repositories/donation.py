from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, User

from .base import BaseCharityRepository


class DonationRepository(BaseCharityRepository):
    async def get_all_by_user(
        self, user: User, session: AsyncSession
    ) -> list[Donation]:
        """Получить список всех пожертвований пользователя."""
        donations_list = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations_list.scalars().all()
