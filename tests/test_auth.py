from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post('/auth/token', data={'username': user.email, 'password': user.clean_password})
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_token_expired_after_time(client, user, token):
    with freeze_time('2025-12-31 12:00:00'):
        response = client.post('/auth/token', data={'username': user.email, 'password': user.clean_password})
        assert response.status_code == HTTPStatus.OK

        token = response.json()['access_token']

    with freeze_time('2025-12-31 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={'username': 'wrong', 'email': 'wrong@wrong', 'password': 'wrongpassword'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_wrong_password(client, user):
    response = client.post('/auth/token', data={'username': user.email, 'password': 'wrooooong'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_inexistent_user(client):
    response = client.post('/auth/token', data={'username': 'wrong@wrong', 'password': 'wrong'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, token):
    response = client.post('auth/refresh-token', headers={'Authorization': f'Bearer {token}'})
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


def test_token_expired_dont_refresh(client, user, token):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh-token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
