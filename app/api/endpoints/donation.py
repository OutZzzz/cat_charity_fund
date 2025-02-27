from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.schemas.donation import DonationCreate, DonationUserDB, DonationSuperUserDB
from app.crud.donation import donation_crud
from app.models import User


router = APIRouter()


@router.get(
        '/',
        response_model=list[DonationSuperUserDB],
        response_model_exclude_none=True,
        dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.\n
    Возвращает список всех пожертвований."""
    all_donations = await donation_crud.get_all(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(
        donation, session, user)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationUserDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    all_donations = await donation_crud.get_my(
        user=user, session=session)
    return all_donations