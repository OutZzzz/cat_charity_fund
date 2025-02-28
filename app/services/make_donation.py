from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, not_

from app.models import Donation, CharityProject


async def get_first_in_donation(
        session: AsyncSession
):
    project = await session.execute(
        select(CharityProject).where(
            not_(CharityProject.fully_invested)).order_by(
                CharityProject.id))
    return project.scalars().first()


async def get_donation_with_free_money(
        session: AsyncSession
):
    project = await session.execute(
        select(Donation).where(
            not_(Donation.fully_invested)).order_by(
                Donation.id))
    return project.scalars().first()


async def make_donation(
        donation: Donation,
        session: AsyncSession
):
    while not donation.fully_invested:
        project = await get_first_in_donation(session)

        if project is None:
            break

        remain = project.full_amount - project.invested_amount
        donation_amount = donation.full_amount - donation.invested_amount
        invested = min(donation_amount, remain)
        donation_remain = donation_amount - invested
        project.invested_amount += invested
        donation.invested_amount += invested
        project.fully_invested = project.invested_amount == project.full_amount
        donation.fully_invested = donation_remain == 0

        if project.fully_invested:
            project.close_date = datetime.now()

        if donation.fully_invested:
            donation.close_date = datetime.now()

        session.add(project)
        session.add(donation)
        await session.commit()
        await session.refresh(project)
        await session.refresh(donation)
