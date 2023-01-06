from fastapi import HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


class Messages:
    duplicate_name = 'Проект с таким именем уже существует!'
    not_found = 'Проект не найден!'
    enough_less_then_before = 'Сумма проекта не может быть меньше внесённой!'
    project_is_closed = 'Закрытый проект нельзя редактировать!'
    project_is_donated = (
        'В проект были внесены средства, не подлежит удалению!'
    )


class CharityProjectValidator:

    @staticmethod
    async def get_if_exists(
            project_id: int,
            session: AsyncSession,
    ) -> CharityProject:
        project = await charity_project_crud.get_by_attribute(
            'id', project_id, session
        )
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=Messages.not_found
            )
        return project

    @staticmethod
    async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
    ) -> None:
        project_id = await charity_project_crud.get_project_id_by_name(
            project_name, session
        )
        if project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Messages.duplicate_name,
            )

    @staticmethod
    def check_project_is_donated(project: CharityProject) -> None:
        if project.invested_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Messages.project_is_donated,
            )

    @staticmethod
    async def is_full_amount(
        amount: PositiveInt,
        project_id: int,
        session: AsyncSession,
    ) -> bool:
        project = await charity_project_crud.get_by_attribute(
            'id', project_id, session
        )
        if amount < project.invested_amount:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=Messages.enough_less_then_before,
            )
        return amount == project.invested_amount

    @staticmethod
    def check_project_is_closed(project: CharityProject) -> None:
        if project.fully_invested:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Messages.project_is_closed,
            )
