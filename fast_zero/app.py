from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI(title='Fast Zero')

database = []


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
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found!'
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    if user_id < 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found!'
        )

    del database[user_id - 1]


@app.get('/users/{user_id}', response_model=UserPublic)
def get_user(user_id: int):
    if user_id < 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found!'
        )

    return database[user_id - 1]
