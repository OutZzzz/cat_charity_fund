from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas import (
    CharityProjectDB, CharityProjectCreate, CharityProjectUpdate)
from app.crud import charity_project_crud, donation_crud
from app.api.validators import (
    check_project_exists, check_name_unique, check_proj_before_delete,
    check_proj_unclose, check_value)
from app.services.make_donation import make_donation

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.\n
    Создаёт благотворительный проект."""
    await check_name_unique(charity_project, session)

    new_project = await charity_project_crud.create(charity_project, session)

    donations = await donation_crud.get_for_invest(session)
    projects = await charity_project_crud.get_for_invest(session)

    await make_donation(
        donations=donations,
        projects=projects,
        session=session)

    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
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
    check_proj_before_delete(project)
    project = await charity_project_crud.delete(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
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
    await check_name_unique(obj_in, session)

    check_proj_unclose(project)

    if obj_in.full_amount:
        check_value(project, obj_in)

    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project
