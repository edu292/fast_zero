from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornat_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_html_deve_retornar_html(client):
    response = client.get('/html')

    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert 'olá mundo' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={'username': 'alice', 'email': 'alice@example.com', 'password': 'secret'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_create_user_username_already_taken(client, user):
    response = client.post(
        '/users/', json={'username': user.username, 'email': 'email@email.com', 'password': 'password'}
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_already_take(client, user):
    response = client.post('/users/', json={'username': 'username', 'email': user.email, 'password': 'password'})

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={'username': 'bob', 'email': 'bob@example.com', 'password': 'secret'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@example.com',
    }


def test_update_user_invalid(client):
    response = client.put(
        '/users/2',
        json={'username': 'bob', 'email': 'bob@example.com', 'password': 'secret'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_user(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'username': 'Test', 'email': 'test@test.com'}


def test_get_user_not_found(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_invalid(client):
    response = client.delete('/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}
