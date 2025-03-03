from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_projects import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def check_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Проект не найден!"
        )
    return project


async def check_name_unique(
        project,
        session: AsyncSession):
    project_name = await charity_project_crud.get_obj_with_same_name(
        project,
        session)
    if project_name is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует.",
        )


def check_proj_before_delete(project: CharityProject):
    if project.fully_invested or (project.invested_amount != 0):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                f"Нельзя удалять закрытый проект или проект, "
                f"в который уже были инвестированы деньги"
            ),
        )


def check_proj_unclose(project: CharityProject):
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                f'Закрытый проект нельзя редактировать'
            )
        )


def check_value(project: CharityProject, updade_data: CharityProjectUpdate):
    if project.invested_amount > updade_data.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                f'Нельзя установить требуемую сумму меньше уже вложенной.'
            )
        )
