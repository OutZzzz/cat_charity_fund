from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, CharityProject


def full_invested(obj: Union[Donation, CharityProject]):
    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()


async def make_donation(
        donations: list[Donation],
        projects: list[CharityProject],
        session: AsyncSession
):

    for donation in donations:
        if donation.fully_invested:
            continue

        for project in projects:
            if project.fully_invested:
                continue

            donation_remain = donation.full_amount - donation.invested_amount
            project_remain = project.full_amount - project.invested_amount

            invest_amount = min(donation_remain, project_remain)

            donation.invested_amount += invest_amount
            project.invested_amount += invest_amount

            full_invested(project)
            full_invested(donation)

            await session.commit()
            await session.refresh(project)
            await session.refresh(donation)

            if donation.fully_invested:
                break
