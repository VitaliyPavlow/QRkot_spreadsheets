from typing import List, Optional, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ObjectIsNoneException
from app.models import CharityProject, Donation, User


ModelType = TypeVar("ModelType")


class BaseRepository:
    def __init__(self, model: ModelType):
        self.model = model

    async def get_list(self, session: AsyncSession) -> List[ModelType]:
        """Получить полный список объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self, obj_in, session: AsyncSession, user: Optional[User] = None
    ) -> ModelType:
        """Создать объект."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data["user_id"] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ) -> ModelType:
        """Удалить объект."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ) -> ModelType:
        """Обновить атрибуты объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_by_attribute(
        self,
        attribute_name,
        search_value,
        session: AsyncSession,
    ) -> ModelType:
        """Получить объект по указанному атрибуту."""
        if hasattr(self.model, attribute_name):
            obj = await session.execute(
                select(self.model).where(
                    getattr(self.model, attribute_name) == search_value
                )
            )
            obj = obj.scalars().first()
            if obj is None:
                raise ObjectIsNoneException()
            return obj


class BaseCharityRepository(BaseRepository):
    async def get_all_open_objects_sorted_by_id(
        self, session: AsyncSession
    ) -> List[Union[CharityProject, Donation]]:
        """Получить список открытых объектов, отсортированных по дате создания."""
        open_objects = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.id)
        )
        return open_objects.scalars().all()
