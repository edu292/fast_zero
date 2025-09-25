from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_deve_retornat_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_html_deve_retornar_html():
    client = TestClient(app)

    response = client.get('/html')

    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert 'olá mundo' in response.text
