from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreateIn(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreateOut(DonationCreateIn):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationCreateOut):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
