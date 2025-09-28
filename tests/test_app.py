from http import HTTPStatus


def test_root_deve_retornat_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_html_deve_retornar_html(client):
    response = client.get('/html')

    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert 'olá mundo' in response.text
