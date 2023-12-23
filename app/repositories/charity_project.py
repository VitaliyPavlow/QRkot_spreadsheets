from typing import List

from sqlalchemy import extract, select

from app.models import CharityProject

from .base import BaseCharityRepository


class CharityProjectRepository(BaseCharityRepository):
    """Операции в БД с моделью CharityProject."""

    async def get_by_completion_rate(self) -> List[CharityProject]:
        """Возвращает отсортированный по времени сбора список проектов."""
        completion_rate = extract("epoch", self.model.close_date) - extract(
            "epoch", self.model.create_date
        )
        async with self.session:
            projects = await self.session.execute(
                select(self.model)
                .filter(self.model.close_date.isnot(None))
                .order_by(completion_rate)
            )
            return projects.scalars().all()
