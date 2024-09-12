from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import db_helper
from . import crud


async def task_by_id(
        task_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    task = await crud.get_task(session=session, task_id=task_id)
    if task is not None:
        return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Task {task_id} not found!'
    )
