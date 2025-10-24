from http import HTTPStatus
from typing import List

from backend.schemas.task import TaskOutSchema
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.database import get_session
from backend.models.users import User, Task
from backend.services.auth import get_auth, Auth


from backend.schemas.task import (
    TaskCreateSchema,
    TaskUpdateSchema,
    TaskStatusSchema,
)


# -------------------- Router -------------------- #
tasks = APIRouter(prefix='/api/tasks', tags=['tasks'])
security = HTTPBearer(auto_error=False)


# -------------------- Helpers -------------------- #
def _safe_dump(model) -> dict:
    """Compat: Pydantic v2 (model_dump) e v1 (dict)."""
    if hasattr(model, 'model_dump'):
        return model.model_dump(exclude_unset=True)
    return model.dict(exclude_unset=True)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: Session = Depends(get_session),
    auth_service: Auth = Depends(get_auth),
) -> User:
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
        email = payload.get('email')
        if not email:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Token inválido: email ausente.',
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Token inválido ou expirado.',
        )

    user = session.scalar(select(User).where(User.email == email))
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado.',
        )
    return user


def _get_task_owned_or_404(session: Session, user: User, task_id: int) -> Task:
    task = session.scalar(
        select(Task).where(Task.id == task_id, Task.user_id == user.id)
    )
    if task is None:
        # Não revelar existência de tarefas de outros usuários
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Tarefa não encontrada.',
        )
    return task


# -------------------- Endpoint -------------------- #
@tasks.get(
    '',
    status_code=HTTPStatus.OK,
    response_model=List[TaskOutSchema],
)
def list_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    rows = (
        session.execute(
            select(Task).where(Task.user_id == current_user.id).order_by(Task.id.desc())
        )
        .scalars()
        .all()
    )
    return rows


@tasks.post(
    '',
    status_code=HTTPStatus.CREATED,
    response_model=TaskOutSchema,
)
def create_task(
    payload: TaskCreateSchema,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    data = _safe_dump(payload)

    task = Task(
        title=data['title'],
        user_id=current_user.id,
        description=data.get('description'),
        priority=data.get('priority'),
        status=data.get('status'),
        due_date=data.get('due_date'),
    )

    if hasattr(task, 'user'):
        task.user = current_user
    else:
        task.user_id = current_user.id  # type: ignore[attr-defined]

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@tasks.get(
    '/{task_id}',
    status_code=HTTPStatus.OK,
    response_model=TaskOutSchema,
)
def get_task_by_id(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = _get_task_owned_or_404(session, current_user, task_id)
    return task


@tasks.put(
    '/{task_id}',
    status_code=HTTPStatus.OK,
    response_model=TaskOutSchema,
)
@tasks.patch(
    '/{task_id}',
    status_code=HTTPStatus.OK,
    response_model=TaskOutSchema,
)
def update_task(
    task_id: int,
    payload: TaskUpdateSchema,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = _get_task_owned_or_404(session, current_user, task_id)
    data = _safe_dump(payload)

    for field in ('title', 'description', 'priority', 'status', 'due_date'):
        if field in data and data[field] is not None:
            setattr(task, field, data[field])

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@tasks.delete(
    '/{task_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = _get_task_owned_or_404(session, current_user, task_id)
    session.delete(task)
    session.commit()
    return None


@tasks.patch(
    '/{task_id}/status',
    status_code=HTTPStatus.OK,
    response_model=TaskOutSchema,
)
def change_task_status(
    task_id: int,
    payload: TaskStatusSchema,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = _get_task_owned_or_404(session, current_user, task_id)
    task.status = payload.status
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
