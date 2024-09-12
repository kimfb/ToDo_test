from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDBModel


class User(BaseDBModel):
    """
    Модель таблицы пользователей.

    Аттрибуты:
        id (int): идентификатор (primary key)
        user_name (str): имя пользователя
        user_surname (str): фамилия пользователя
        task (relationship): связь (один ко многим) с таблицей task

    Таблица:
        __tablename__ = 'user'

    """
    __tablename__ = 'user'

    user_name: Mapped[Optional[str]]
    user_surname: Mapped[Optional[str]]
    task = relationship('Task', back_populates='user')


class Task(BaseDBModel):
    """
    Модель таблицы задач.

    Аттрибуты:
        id (int): идентификатор (primary key)
        user_id (int): идентификатор пользователя (foreign key)
        title (str): заголовок задачи
        description (str): описание задачи
        created_at (datetime): время создания
        updated_at (datetime): время обновления
        user (relationship): связь с таблицей user

    Таблица:
        __tablename__ = 'task'
    """
    __tablename__ = 'task'

    title: Mapped[str]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    created_at: Mapped[datetime]
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    user = relationship('User', back_populates='task')

