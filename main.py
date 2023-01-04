from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user
from auth.schemas import Token
from sql_app.database import get_session
from sql_app import crud
from sql_app import schemas

app = FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: AsyncSession = Depends(get_session)):
    user = await authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.User)
async def read_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@app.post("/users/create", status_code=201, response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_session)):
    created_user = await crud.create_user(db, user)
    return created_user
