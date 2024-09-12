"""
Create
Read
Update
Delete
"""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.tables import User, Task
from api.shemas.tasks import TaskCreate, TaskUpdate


async def create_task(session: AsyncSession, task_in: TaskCreate):
    """Создание новой задачи."""
    user_cur = select(User).where(
        User.user_name == task_in.user_name,
        User.user_surname == task_in.user_surname
    )

    result = await session.execute(user_cur)
    user_cur = result.scalar_one_or_none()

    if user_cur is None:
        user_cur = User(user_name=task_in.user_name, user_surname=task_in.user_surname)
        session.add(user_cur)
        await session.flush()

    task = Task(
        title=task_in.title,
        description=task_in.description,
        user_id=user_cur.id,
        created_at=datetime.now()
    )
    session.add(task)
    await session.commit()
    return task


async def get_tasks_by_user(session: AsyncSession, user_id: int):
    """Получение списка задач отдельного пользователя."""
    stmt = select(Task).options(joinedload(Task.user)).where(Task.user_id == user_id)
    result = await session.execute(stmt)
    tasks = result.scalars().all()
    tasks_list = to_form_response(tasks)

    return tasks_list


async def get_all_tasks(session: AsyncSession):
    """Получение списка задач всех пользователей"""
    stmt = select(Task).options(joinedload(Task.user)).order_by(Task.id)
    result = await session.execute(stmt)
    tasks = result.scalars().all()
    tasks_list = to_form_response(tasks)

    return tasks_list


async def get_task(session: AsyncSession, task_id: int):
    """ Получение информации о задаче по id."""
    # stmt = select(Task).where(Task.id == task_id)
    return await session.get(Task, task_id)


async def update_task(
    session: AsyncSession,
    task: Task,
    task_update: TaskUpdate,
    partial: bool = False
):
    """ Полное или частичное обновление полей задачи по id."""
    for name, value in task_update.model_dump(exclude_unset=partial).items():
        setattr(task, name, value)
    setattr(task, "updated_at", datetime.now())
    await session.commit()
    return task


async def delete_task(
        session: AsyncSession,
        task: Task
):
    """Удаление задачи по id."""
    await session.delete(task)
    await session.commit()
    return [{"status": "Task successfully deleted!"}]


def to_form_response(tasks):
    """Побочная функция для формирования словаря данных для вывода."""
    tasks_list = [{"message": 'User not Found'}]
    if tasks:
        tasks_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "user_name": task.user.user_name,
                "user_surname": task.user.user_surname
            }
            for task in tasks
        ]
    return tasks_list
