from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'email': 'alice@example.com',
                'username': 'alice',
            },
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret'
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
            'id': 1,
            'username': 'bob',
            'email': 'bob@example.com',
        }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.NO_CONTENT
