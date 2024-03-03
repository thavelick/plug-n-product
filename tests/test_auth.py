import pytest
from flask import g, session
from application.db import get_db_connection


def test_register(client, app):
    assert client.get("/register").status_code == 200
    response = client.post(
        "/register",
        data={"email": "a@example.com", "password": "a-decently-long-password"},
    )
    assert response.headers["Location"] == "/sign-in"

    with app.app_context():
        assert (
            get_db_connection()
            .execute(
                "SELECT * FROM user WHERE email = 'a@example.com'",
            )
            .fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("email", "password", "message"),
    (
        ("", "", b"Email is required."),
        ("a@example.com", "", b"Password is required."),
        ("test@example.com", "a-decently-long-password", b"already registered"),
        ("test@example.com", "short", b"Password must be at least 10 characters long."),
    ),
)
def test_register_validate_input(client, email, password, message):
    response = client.post("/register", data={"email": email, "password": password})
    assert message in response.data


def test_signin(client, auth):
    assert client.get("/sign-in").status_code == 200
    response = auth.signin()
    assert response.headers["Location"] == "/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user.email == "test@example.com"


def test_session_with_invalid_user_id(client, auth, app):
    # First, sign in as a user, then manually delete the user from the database
    # and try to get the home page. The user should be logged out.

    auth.signin()

    with app.app_context():
        with get_db_connection() as connection:
            connection.execute("DELETE FROM user WHERE id = 1")

    with client:
        assert "Sign-in" in client.get("/").data.decode("utf-8")


@pytest.mark.parametrize(
    ("email", "password", "message"),
    (
        (
            "a@example.com",
            "test",
            b"Error! Could not sign in. Please check your credentials and try again.",
        ),
        (
            "test@example.com",
            "a",
            b"Error! Could not sign in. Please check your credentials and try again.",
        ),
    ),
)
def test_signin_validate_input(auth, email, password, message):
    response = auth.signin(email, password)
    assert message in response.data


def test_signout(client, auth):
    auth.signin()

    with client:
        auth.logout()
        assert "user_id" not in session


@pytest.mark.parametrize(
    ("path", "show_password", "expected_type"),
    (
        ("/register/password", "on", "text"),
        ("/register/password", None, "password"),
        ("/sign-in/password", "on", "text"),
        ("/sign-in/password", None, "password"),
    ),
)
def test_password_field(client, path, show_password, expected_type):
    response = client.post(
        path, data={"show_password": show_password, "password": "test"}
    )
    assert f'type="{expected_type}"'.encode() in response.data
    assert b'value="test"' in response.data
