from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer


class AmountDateMixin:
    """Общие поля для моделей."""

    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)
