from dataclasses import asdict
from datetime import date
from sqlalchemy import select

from backend.models.users import Task, TaskStatus, TaskPriority
from backend.models.users import User


def _create_user(session) -> User:
    user = User(
        name='Benjamin Silva',
        email='benjamin.silva@email.com',
        hashed_password='hashed_password',
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_create_task_defaults(session, mock_db_time):
    user = _create_user(session)

    with mock_db_time(model=Task) as mocked_time:
        new_task = Task(
            title='Pagar boletos',
            user_id=user.id,
        )
        session.add(new_task)
        session.commit()

    task = session.scalar(select(Task).where(Task.title == 'Pagar boletos'))

    data = asdict(task)
    data.pop('user', None)

    assert data == {
        'id': 1,
        'title': 'Pagar boletos',
        'description': None,
        'status': TaskStatus.PENDENTE,
        'priority': TaskPriority.MEDIA,
        'due_date': None,
        'created_at': mocked_time,
        'updated_at': mocked_time,
        'user_id': user.id,
    }


def test_create_task_full_fields(session, mock_db_time):
    user = _create_user(session)
    venc = date(2025, 1, 31)

    with mock_db_time(model=Task) as mocked_time:
        new_task = Task(
            title='Entregar relatório',
            description='Relatório mensal de desempenho',
            status=TaskStatus.CONCLUIDA,
            priority=TaskPriority.ALTA,
            due_date=venc,
            user_id=user.id,
        )
        session.add(new_task)
        session.commit()

    task = session.scalar(select(Task).where(Task.title == 'Entregar relatório'))

    data = asdict(task)
    data.pop('user', None)

    assert (
        data
        == {
            'id': 1,  # banco limpo para teste;
            'title': 'Entregar relatório',
            'description': 'Relatório mensal de desempenho',
            'status': TaskStatus.CONCLUIDA,
            'priority': TaskPriority.ALTA,
            'due_date': venc,
            'created_at': mocked_time,
            'updated_at': mocked_time,
            'user_id': user.id,
        }
    )


def test_task_user_relationship_backref(session, mock_db_time):
    user = _create_user(session)

    with mock_db_time(model=Task):
        t1 = Task(title='Task A', user_id=user.id)
        t2 = Task(title='Task B', user_id=user.id)
        session.add_all([t1, t2])
        session.commit()


    session.refresh(user)
    titles = sorted([t.title for t in user.tasks])
    assert titles == ['Task A', 'Task B']


    count = session.scalars(select(Task).where(Task.user_id == user.id)).all()
    assert len(count) == 2
