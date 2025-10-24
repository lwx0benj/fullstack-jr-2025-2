from http import HTTPStatus

from sqlalchemy import select

from backend.models.users import User, Task
from backend.services.auth import Auth


# --- helpers ---


def _create_user(
    session, *, name='Ada Lovelace', email='ada@example.com', password='S3nh@F0rte'
):
    auth = Auth()
    hashed = auth.hash_password(password)
    user = User(name=name, email=email, hashed_password=hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def _login_and_get_token(client, *, email: str, password: str) -> str:
    resp = client.post('/api/auth/login', json={'email': email, 'password': password})
    assert resp.status_code == HTTPStatus.OK
    return resp.json()['access_token']


def _create_task(
    session, *, 
    title='Comprar pão', user_id: int, description='Integral', status=None, priority=None, due_date=None
):
    task = Task(
        title=title, 
        user_id=user_id, 
        description=description, 
        status=status, priority=priority, 
        due_date=due_date)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# --- GET /api/tasks ---


def test_get_task_by_id_success_returns_task(client, session):
    # Arrange: usuário e tarefa dele
    user = _create_user(session)
    token = _login_and_get_token(client, email=user.email, password='S3nh@F0rte')
    task = _create_task(
        session,
        user_id=user.id,
        title='Estudar testes',
        description='pytest + httpx',
        status=None,
        priority=None,
        due_date=None,
    )

    # Act
    resp = client.get(
        '/api/tasks',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert resp.status_code == HTTPStatus.OK
    list_data = resp.json()
    data = list_data[0]

    assert data['id'] == task.id
    assert data['title'] == 'Estudar testes'
    assert data.get('description') == 'pytest + httpx'


def test_get_task_by_id_missing_token_returns_401(client, session):
    # Arrange: tarefa existe, mas sem Authorization header
    user = _create_user(session, email='ada2@example.com')
    task = _create_task(session, user_id=user.id)

    # Act
    resp = client.get(f'/api/tasks/{task.id}')

    # Assert
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    body = resp.json()
    assert (
        body.get('detail')
        == 'Token ausente ou esquema inválido. Use Authorization: Bearer <token>.'
    )


def test_get_task_by_id_not_found_when_task_does_not_exist_returns_404(client, session):
    # Arrange: usuário autenticado, id inexistente
    user = _create_user(session, email='ada3@example.com')
    token = _login_and_get_token(client, email=user.email, password='S3nh@F0rte')

    nonexistent_id = 999_999
    assert session.get(Task, nonexistent_id) is None

    # Act
    resp = client.get(
        f'/api/tasks/{nonexistent_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert resp.status_code == HTTPStatus.NOT_FOUND
    body = resp.json()
    assert body.get('detail') in {'Tarefa não encontrada.', 'Task not found.'}


def test_get_task_by_id_not_found_when_task_belongs_to_another_user_returns_404(
    client, session
):
    # Arrange: duas pessoas; tarefa pertence à outra
    owner = _create_user(session, email='owner@example.com')
    stranger = _create_user(session, email='stranger@example.com')
    task = _create_task(session, user_id=owner.id, title='Tarefa privada')

    token = _login_and_get_token(client, email=stranger.email, password='S3nh@F0rte')

    # Act
    resp = client.get(
        f'/api/tasks/{task.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert resp.status_code == HTTPStatus.NOT_FOUND
    body = resp.json()
    assert body.get('detail') in {'Tarefa não encontrada.', 'Task not found.'}


# --- POST /api/tasks ---

def test_create_task_success_persists_and_returns_task(client, session):
    # Arrange
    user = _create_user(session)
    token = _login_and_get_token(client, email=user.email, password="S3nh@F0rte")

    payload = {
        "title": "Estudar Pytest",
        "description": "Cobrir create_task",
        "priority": "alta",
        "status": "pendente",
        "due_date": "2025-12-31",
    }

    # Act
    resp = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )

    # Assert
    assert resp.status_code == HTTPStatus.CREATED
    data = resp.json()

    assert isinstance(data.get("id"), int)
    assert data["title"] == payload["title"]
    assert data.get("description") == payload["description"]
    assert data.get("priority") == payload["priority"]
    assert data.get("status") == payload["status"]
    assert data.get("due_date") in {"2025-12-31", "2025-12-31T00:00:00"}  # depende do schema

    db_task = session.get(Task, data["id"])
    assert db_task is not None
    assert db_task.title == payload["title"]
    assert getattr(db_task, "description", None) == payload["description"]
    assert getattr(db_task, "priority", None) == payload["priority"]
    assert getattr(db_task, "status", None) == payload["status"]
    assert str(getattr(db_task, "due_date", ""))[:10] == "2025-12-31"

    if hasattr(db_task, "user"):
        assert db_task.user.id == user.id
    else:
        assert getattr(db_task, "user_id") == user.id


def test_create_task_without_optional_fields_sets_nulls(client, session):
    # Arrange
    user = _create_user(session, email="ada2@example.com")
    token = _login_and_get_token(client, email=user.email, password="S3nh@F0rte")

    payload = {
        "title": "Tarefa com título",
        "status": "pendente",
        "priority": "alta",
    }

    # Act
    resp = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )

    # Assert
    assert resp.status_code == HTTPStatus.CREATED
    data = resp.json()
    assert data["title"] == payload["title"]
 
    assert data.get("description") in (None, "")
    assert data.get("priority") in (None, "alta")
    assert data.get("status") in (None, "pendente")
    assert data.get("due_date") in (None, "")

    db_task = session.get(Task, data["id"])
    assert db_task is not None
    assert getattr(db_task, "description", None) in (None, "")
    assert getattr(db_task, "priority", None) in (None, "alta")
    assert getattr(db_task, "status", None) in (None, "pendente")
    assert getattr(db_task, "due_date", None) in (None, "")


def test_create_task_missing_token_returns_401(client, session):
    # Arrange
    assert session.scalars(select(Task)).all() == []

    payload = {"title": "Sem token"}

    # Act
    resp = client.post("/api/tasks", json=payload)

    # Assert
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    body = resp.json()
    assert body.get("detail") == "Token ausente ou esquema inválido. Use Authorization: Bearer <token>."
    # nada persistido
    assert session.scalars(select(Task)).all() == []


def test_create_task_with_wrong_scheme_returns_401(client, session):
    # Arrange
    _create_user(session, email="ada3@example.com")
    payload = {"title": "Header errado"}

    # Act
    resp = client.post(
        "/api/tasks",
        headers={"Authorization": "Basic abc.def.ghi"},
        json=payload,
    )

    # Assert
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    body = resp.json()
    assert body.get("detail") == "Token ausente ou esquema inválido. Use Authorization: Bearer <token>."
