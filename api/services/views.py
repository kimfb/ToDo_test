from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import db_helper
from api.shemas import Task, TaskCreate, TaskUpdate
from .dependencies import task_by_id
from . import crud


router = APIRouter(tags=['Tasks'], prefix='/tasks')


@router.post("/create", response_model=Task)
async def task_create(
        task_in: TaskCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_task(session=session, task_in=task_in)


@router.get('/all')
async def get_task_by_user(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_tasks(session=session)


@router.get('/{task_id}', response_model=Task)
async def get_task(
        task: Task = Depends(task_by_id),
):
    return task


@router.get('/users/{user_id}')
async def get_task_by_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_tasks_by_user(session=session, user_id=user_id)


@router.patch("/{task_id}")
async def update_product_partial(
    task_update: TaskUpdate,
    task: Task = Depends(task_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_task(
        session=session,
        task=task,
        task_update=task_update,
        partial=True,
    )


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(
        task: Task = Depends(task_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.delete_task(session=session, task=task)
