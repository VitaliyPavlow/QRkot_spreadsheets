from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base

from .common import AmountDateMixin


class Donation(Base, AmountDateMixin):
    """Модель для объектов пожертвований."""

    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)
