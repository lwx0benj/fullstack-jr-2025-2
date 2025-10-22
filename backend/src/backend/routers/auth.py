from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.database import get_session
from backend.models.users import User
from backend.schemas.auth import (
    UserPublicSchema,
    UserRegisterSchema,
)

auth = APIRouter(prefix='/api/auth', tags=['auth'])


@auth.post(
    path='/register',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublicSchema,
)
def register(
    user: UserRegisterSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.email == user.email))

    if db_user is not None:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Usuário já cadastrado.',
            )

    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=user.password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
