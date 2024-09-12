from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session
)

from core.config import settings


class DataBase:
    """
     Класс управления подключением к базе данных и созданием сессий.

     Attributes:
        engine (AsyncEngine): асинхронный движок базы данных.
        session_factory (sessionmaker): фабрика асинхронных сессий.

     Methods:
        __init__(url: str, echo: bool = False): инициализирует движок БД и фабрику сессий.
        get_scoped_session() -> scoped_session: создает и возвращает асинхронную scoped-сессию.
        scoped_session_dependency() -> AsyncIterator[scoped_session]: генератор для создания scoped-сессии.
    """
    def __init__(self, url: str, echo: bool = False):
        """ Инициализирует движок БД и фабрику сессий (async)."""
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def get_scoped_session(self):
        """
        Создает и возвращает асинхронную scoped-сессию.

        Returns:
            scoped_session: экземпляр синхронной scoped-сессии, привязанный
        к текущей задаче.
        """
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session

    async def scoped_session_dependency(self):
        """
        Генератор для создания scoped-сессии.

        Returns:
            AsyncIterator[scoped_session]: Асинхронный генератор,
        предоставляющий scoped-сессию.
        """
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DataBase(
    url=settings.db_url,
    echo=settings.db_echo
)
