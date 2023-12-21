from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreateIn(BaseModel):
    """Pydantic схема для валидации входящих донатов."""

    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreateOut(DonationCreateIn):
    """Схема для сериализации донатов при создании."""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationCreateOut):
    """Схема для БД."""

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
