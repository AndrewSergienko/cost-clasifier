from sqlalchemy.orm import declarative_base
from config import Config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


DATABASE_URL = Config.DB_CONFIG
engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
