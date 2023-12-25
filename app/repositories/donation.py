from sqlalchemy import select

from app.models import Donation, User

from .base import BaseCharityRepository


class DonationRepository(BaseCharityRepository):
    async def get_all_by_user(self, user: User) -> list[Donation]:
        """Получить список всех пожертвований пользователя."""
        async with self.session as session:
            donations_list = await session.execute(
                select(Donation).where(Donation.user_id == user.id)
            )
            return donations_list.scalars().all()
