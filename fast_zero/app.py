from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routes import auth, users
from fast_zero.schemas import Message

app = FastAPI(title='Fast Zero')

app.include_router(users.router)
app.include_router(auth.router)


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
