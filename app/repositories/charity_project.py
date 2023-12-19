from typing import List

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject

from .base import BaseCharityRepository


class CharityProjectRepository(BaseCharityRepository):
    """Операции в БД с моделью CharityProject."""

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> List[CharityProject]:
        """Возвращает отсортированный по времени сбора список проектов."""
        completion_rate = extract("epoch", self.model.close_date) - extract(
            "epoch", self.model.create_date
        )
        projects = await session.execute(
            select(self.model).order_by(completion_rate)
        )
        return projects.scalars().all()
