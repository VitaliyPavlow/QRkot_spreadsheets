from typing import List, Optional, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ObjectIsNoneException
from app.models import CharityProject, Donation, User


ModelType = TypeVar("ModelType")


class BaseRepository:
    def __init__(self, model: ModelType, session: AsyncSession):
        self.model = model
        self.session = session

    async def get_list(self) -> List[ModelType]:
        """Получить полный список объектов."""
        async with self.session:
            db_objs = await self.session.execute(select(self.model))
            return db_objs.scalars().all()

    async def create(self, obj_in, user: Optional[User] = None) -> ModelType:
        """Создать объект."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data["user_id"] = user.id
        db_obj = self.model(**obj_in_data)
        async with self.session:
            self.session.add(db_obj)
            await self.session.commit()
            await self.session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj) -> ModelType:
        """Удалить объект."""
        async with self.session:
            await self.session.delete(db_obj)
            await self.session.commit()
        return db_obj

    async def update(self, db_obj, obj_in) -> ModelType:
        """Обновить атрибуты объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        async with self.session:
            self.session.add(db_obj)
            await self.session.commit()
            await self.session.refresh(db_obj)
        return db_obj

    async def refresh(self, obj_in: ModelType) -> ModelType:
        async with self.session:
            self.session.add(obj_in)
            await self.session.refresh(obj_in)
            return obj_in

    async def get_by_attribute(
        self, attribute_name, search_value
    ) -> ModelType:
        """Получить объект по указанному атрибуту."""
        try:
            async with self.session:
                obj = await self.session.execute(
                    select(self.model).where(
                        getattr(self.model, attribute_name) == search_value
                    )
                )
                obj = obj.scalars().first()
            if obj is None:
                raise ObjectIsNoneException()
            return obj
        except AttributeError:
            raise ObjectIsNoneException()


class BaseCharityRepository(BaseRepository):
    async def get_all_open_objects_sorted_by_id(
        self,
    ) -> List[Union[CharityProject, Donation]]:
        """Получить список открытых объектов, отсортированных по дате создания."""
        async with self.session:
            open_objects = await self.session.execute(
                select(self.model)
                .where(self.model.fully_invested.is_(False))
                .order_by(self.model.id)
            )
            return open_objects.scalars().all()
