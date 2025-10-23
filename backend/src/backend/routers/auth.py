from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.database import get_session
from backend.models.users import User
from backend.schemas.auth import (
    Token, 
    UserRegisterSchema,
    UserLoginSchema,
    UserInfoSchema,
)

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


@auth.post(
    path='/login',
    status_code=HTTPStatus.OK,
    response_model=Token,
)
def login(
    credentials: UserLoginSchema,
    session: Session = Depends(get_session),
    auth_service: Auth = Depends(get_auth),
):

    db_user = session.scalar(select(User).where(User.email == credentials.email))
    if db_user is None:

        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Credenciais inválidas.',
        )


    if not auth_service.verify_password(credentials.password, db_user.hashed_password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Credenciais inválidas.',
        )

    tokens = auth_service.generate_token(
        subject=db_user.id,
        extra_claims={"email": db_user.email, "name": db_user.name},
    )

    return Token(**tokens)


@auth.get(
    path='/userinfo',
    status_code=HTTPStatus.OK,
    response_model=UserInfoSchema,
)
def userinfo(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer(auto_error=False)),
    session: Session = Depends(get_session),
    auth_service: Auth = Depends(get_auth),
):
    if not credentials or credentials.scheme.lower() != 'bearer':
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Token ausente ou esquema inválido. Use Authorization: Bearer <token>.',
        )

    token = credentials.credentials

    try:
        ok, payload, _ = auth_service.verify_token(token)
        if not ok:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Token inválido ou expirado.',
            )
        
        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Token inválido: subject ausente.',
            )
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Token inválido ou expirado.',
        )

    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado.',
        )

    return UserInfoSchema(id=user.id, name=user.name, email=user.email)