from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import Todo, User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='test', email='test@test', password='secret')

        session.add(new_user)
        await session.commit()

        user = await session.scalar(select(User).where(User.username == 'test'))

        assert asdict(user) == {
            'id': 1,
            'username': 'test',
            'email': 'test@test',
            'password': 'secret',
            'created_at': time,
            'updated_at': time,
            'todos': [],
        }


@pytest.mark.asyncio
async def test_create_todo(session, user):
    todo = Todo(title='Test', description='Test', state='Wrong', user_id=user.id)
    session.add(todo)
    await session.commit()

    with pytest.raises(LookupError):
        await session.scalar(select(Todo))
