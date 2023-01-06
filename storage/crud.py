from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from auth.encrypt import get_password_hash
from storage.models.account import User, ManualManager, ApiManager
from storage.schemas import account as account_schemas


async def get_user(db: AsyncSession, user_id: int):
    query = select(User).filter(User.id == user_id)
    return await db.scalar(query)


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).filter(User.email == email).limit(1)
    return await db.scalar(query)


async def create_user(db: AsyncSession, user: account_schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    return db_user


async def create_manual_manager(db: AsyncSession, user: User):
    manager = ManualManager()
    user.manual_manager = manager
    db.add(manager)
    await db.commit()
    return manager


async def create_api_manager(db: AsyncSession, user: User, create_func, *args, **kwargs):
    bank_api_manager = create_func(*args, **kwargs)
    bank_api_manager.user_id = user.id
    db.add(bank_api_manager)
    await db.commit()
    return bank_api_manager




