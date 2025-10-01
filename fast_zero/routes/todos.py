from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import FilterTodo, TodoList, TodoPublic, TodoSchema, TodoUpdate
from fast_zero.security import get_current_user

Session = Annotated[AsyncSession, Depends(get_session)]
User = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', response_model=TodoPublic)
async def create_todo(todo: TodoSchema, session: Session, current_user: User):
    db_todo = Todo(user_id=current_user.id, title=todo.title, description=todo.description, state=todo.state)
    session.add(db_todo)

    await session.commit()
    await session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
async def list_todos(session: Session, user: User, todo_filter: Annotated[FilterTodo, Query()]):
    query = select(Todo).where(Todo.user_id == user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))
    if todo_filter.description:
        query = query.filter(Todo.description.contains(todo_filter.description))
    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = await session.scalars(query.limit(todo_filter.limit).offset(todo_filter.offset))

    return TodoList(todos=todos.all())


@router.delete('/{todo_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_todo(todo_id: int, session: Session, user: User):
    todo = await session.scalar(select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id))

    if not todo:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Task not found')

    await session.delete(todo)
    await session.commit()


@router.patch('/{todo_id}', status_code=HTTPStatus.NO_CONTENT)
async def patch_todo(todo_id: int, session: Session, user: User, todo: TodoUpdate):
    todo_db = await session.scalar(select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id))

    if not todo_db:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Task not found')

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(todo_db, key, value)

    session.add(todo_db)
    await session.commit()


@router.get('/{todo_id}')
async def get_todo(todo_id: int, session: Session, user: User):
    todo_db = await session.scalar(select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id))

    if not todo_db:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='Task not found')

    return todo_db
