from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert 'FastAPI' in response.text


def test_rates():
    response = client.get('/rates')
    data = response.json()
    assert len(data) > 0
    assert 'url' in data[0]
    assert data[0]['buy_price'] != data[0]['sell_price']
    assert data[0]['buy_price'] > 0
