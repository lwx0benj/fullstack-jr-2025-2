from sqlalchemy import func, Enum as SAEnum, ForeignKey, Index
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
    registry,
)

import enum
from datetime import date, datetime


table_registry = registry()


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


# Reutilize o mesmo registry já definido:
# table_registry = registry()


class TaskStatus(str, enum.Enum):
    PENDENTE = 'pendente'
    CONCLUIDA = 'concluida'


class TaskPriority(str, enum.Enum):
    BAIXA = 'baixa'
    MEDIA = 'media'
    ALTA = 'alta'


@mapped_as_dataclass(table_registry)
class Task:
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    description: Mapped[str | None] = mapped_column(default=None)

    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, name='status_tarefa'),
        default=TaskStatus.PENDENTE,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SAEnum(TaskPriority, name='prioridade_tarefa'),
        default=TaskPriority.MEDIA,
    )
    due_date: Mapped[date | None] = mapped_column(default=None)

    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped['User'] = relationship(init=False, backref='tasks')

    __table_args__ = (
        Index(
            'ix_tasks_status_priority', 'status', 'priority'
        ),  # ajuste o nome conforme o teste
    )
