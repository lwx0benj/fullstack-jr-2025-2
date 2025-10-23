from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.database import get_session
from backend.models.users import User
from backend.schemas.auth import Token, UserRegisterSchema
from backend.services.auth import get_auth, Auth

auth = APIRouter(prefix='/api/auth', tags=['auth'])


@auth.post(
    path='/register',
    status_code=HTTPStatus.CREATED,
    response_model=Token,
)
def register(
    user: UserRegisterSchema, 
    session: Session = Depends(get_session),
    auth_service: Auth = Depends(get_auth)
):
    db_user = session.scalar(select(User).where(User.email == user.email))

    if db_user is not None:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Usuário já cadastrado.',
            )

    auth_service = Auth()
    hashed_password = auth_service.hash_password(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    tokens = auth_service.generate_token(
        subject=db_user.id,
        extra_claims={"email": db_user.email},
    )


    return Token(**tokens)
