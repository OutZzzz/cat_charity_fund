from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder

from app.models import CharityProject
from app.schemas import CharityProjectCreate
from .base import CRUDBase


class CRUDCharityProject(CRUDBase):

    async def delete(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        if 'full_amount' in update_data:
            if obj_data["invested_amount"] == update_data["full_amount"]:
                update_data["fully_invested"] = True
                update_data["close_date"] = datetime.now()

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_obj_with_same_name(
            self,
            obj_in: CharityProjectCreate,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.name == obj_in.name
            )
        )
        return db_obj.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
