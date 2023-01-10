import time

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from auth.encrypt import get_password_hash
from storage.models.account import User, ManualManager
from storage.models.operation import ManualOperation
from storage.schemas import account as account_schemas
from storage.schemas.operation import OperationBase


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


async def get_operations(db: AsyncSession, user: User) -> list[ManualOperation]:
    manager_id = await db.scalar(select(ManualManager.id).filter(ManualManager.user_id == user.id))
    operations = await db.scalars(select(ManualOperation).filter(ManualOperation.manager_id == manager_id))
    return operations


async def create_manual_operation(operation: OperationBase, db: AsyncSession, user: User):
    manager_id = await db.scalar(select(ManualManager.id).filter(ManualManager.user_id == user.id))
    new_operation = ManualOperation(
        description=operation.description,
        amount=operation.amount,
        mcc=operation.mcc,
        unix_time=int(time.time()),
        manager_id=manager_id
    )
    db.add(new_operation)
    await db.commit()
    return await db.scalar(select(ManualOperation).filter(ManualOperation.manager_id == manager_id)
                           .order_by(ManualOperation.id.desc()).limit(1))

