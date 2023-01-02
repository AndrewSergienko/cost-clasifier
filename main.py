from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sql_app.database import get_session
from sql_app import crud
from sql_app import schemas

app = FastAPI()


@app.get("/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not exist")
    return user


@app.post("/users/create", status_code=201, response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_session)):
    created_user = await crud.create_user(db, user)
    return created_user
