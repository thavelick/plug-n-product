from application import create_app


def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_home(client):
    response = client.get("/")
    assert "Welcome!" in response.data.decode("utf-8")


def test_home_signed_in(client, auth):
    auth.signin()
    response = client.get("/")
    assert "test@example.com" in response.data.decode("utf-8")
