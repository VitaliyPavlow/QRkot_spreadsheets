from sqlalchemy import Column, String, Text

from app.core.db import Base

from .common import AmountDateMixin


class CharityProject(Base, AmountDateMixin):
    """Модель для проектов сбора пожертвований."""

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
