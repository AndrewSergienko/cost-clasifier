from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models
from . import schemas


async def get_user(db: AsyncSession, user_id: int):
    query = select(models.User).filter(models.User.id == user_id)
    return await db.scalar(query)


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(models.User).filter(models.User.email == email).limit(1)
    return await db.scalar(query)


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    await db.commit()
    return db_user


