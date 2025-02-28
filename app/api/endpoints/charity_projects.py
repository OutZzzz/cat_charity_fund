from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charityproject import (
    CharityProjectDB, CharityProjectCreate, CharityProjectUpdate)
from app.crud.charity_projects import charity_project_crud
from app.api.validators import check_project_exists
from app.services.make_donation import (
    get_donation_with_free_money, make_donation)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.\n
    Создаёт благотворительный проект."""
    new_project = await charity_project_crud.create(charity_project, session)
    donation = await get_donation_with_free_money(session)
    if donation is not None:
        await make_donation(donation, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список всех проектов."""
    all_projects = await charity_project_crud.get_all(session)
    return all_projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.\n
    Удаляет проект. Нельзя удалить проект, в который уже
    были инвестированы средства, его можно только закрыть.
    """
    project = await check_project_exists(
        project_id=project_id, session=session)
    project = await charity_project_crud.delete(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    #dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.\n
    Закрытый проект нельзя редактировать; нельзя установить
    требуемую сумму меньше уже вложенной."""
    project = await check_project_exists(
        project_id=project_id, session=session
    )

    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project