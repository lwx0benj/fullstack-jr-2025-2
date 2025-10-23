from dataclasses import asdict

from sqlalchemy import select

from backend.models.users import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as mocked_time:
        new_user = User(
            name='Benjamin Silva',
            email='benjamin.silva@email.com',
            hashed_password='hashed_password',
        )

        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.email == 'benjamin.silva@email.com'))

    assert asdict(user) == {
        'id': 1,
        'name': 'Benjamin Silva',
        'email': 'benjamin.silva@email.com',
        'hashed_password': 'hashed_password',
        'created_at': mocked_time,
        'updated_at': mocked_time,
    }
