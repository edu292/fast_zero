import asyncio
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routes import auth, todos, users
from fast_zero.schemas import Message

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
app = FastAPI(title='Fast Zero')

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get('/', response_model=Message)
async def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/html', response_class=HTMLResponse)
async def html():
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
