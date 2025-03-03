from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import CharityProject
from .base import CRUDBase


class CRUDCharityProject(CRUDBase):

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
            obj_in,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.name == obj_in.name
            )
        )
        return db_obj.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
