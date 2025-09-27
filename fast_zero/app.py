from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI(title='Fast Zero')


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/html', response_class=HTMLResponse)
def html():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale-1.0">
        <title>HTML</title>
    </head>
    <body>
        <h1>olá mundo!</h1>
    </body>
    <html>
    """


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(HTTPStatus.CONFLICT, detail='Username already exists')
        elif db_user.email == user.email:
            raise HTTPException(HTTPStatus.CONFLICT, detail='Email already exists')

    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(offset=0, limit=10, session: Session = Depends(get_session)):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    user_db: User = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='User not found')

    try:
        user_db.email = user.email
        user_db.username = user.username
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        raise HTTPException(HTTPStatus.CONFLICT, detail='Username or Email already exists')


@app.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='User not found')

    session.delete(user_db)
    session.commit()


@app.get('/users/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='User not found')

    return user_db
