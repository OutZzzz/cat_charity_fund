from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Donation, User
from .base import CRUDBase


class CRUDDonation(CRUDBase):

    async def get_my(
            self,
            user: User,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return db_obj.scalars().all()


donation_crud = CRUDDonation(Donation)
