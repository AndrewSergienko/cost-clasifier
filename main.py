from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import authenticate_user, create_access_token, get_current_user
from auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth.schemas import Token
from bankapi.monobank.crud import create_monobank_manager
from storage.crud import create_manual_manager, create_api_manager, get_operations, create_manual_operation
from storage.database import get_session
from storage import crud
from storage.models.operation import ManualOperation
from storage.schemas import account as user_schemas
from storage.models.account import User
from storage.schemas.operation import OperationBase, OperationReadBase

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


@app.get("/users/me", response_model=user_schemas.User)
async def read_me(current_user: user_schemas.User = Depends(get_current_user)):
    return current_user


@app.post("/users/create", status_code=201, response_model=user_schemas.User)
async def create_user(user_form: user_schemas.UserCreate, db: AsyncSession = Depends(get_session)):
    created_user = await crud.create_user(db, user_form)
    await create_manual_manager(db, created_user)
    return created_user


@app.post("/managers/create_api", status_code=201)
async def create_api_manager_view(params: dict[str, object], db: AsyncSession = Depends(get_session),
                                  user: User = Depends(get_current_user)):
    manager_factories = {
        'monobank': {"callable": create_monobank_manager, "args": ['token']}
    }

    if validate_createapi_params(params, manager_factories):
        await create_api_manager(db, user, manager_factories[params['type']]['callable'], **params)
        return {'status': 'ok'}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/operations", status_code=200, response_model=list[OperationReadBase])
async def read_operations(db: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    operations = list(map(ManualOperation.as_dict, await get_operations(db, user)))
    return operations


@app.post("/operations/add", status_code=201)
async def add_operation(operation: OperationBase, db: AsyncSession = Depends(get_session),
                        user: User = Depends(get_current_user)):
    return await create_manual_operation(operation, db, user)


def validate_createapi_params(params, factories) -> bool:
    return 'type' in params.keys() and \
        params['type'] in factories.keys() and \
        all(list(map(lambda arg: arg in params.keys(), factories[params['type']]['args'])))
