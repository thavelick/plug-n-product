import sqlite3
import tempfile
import os

import pytest

from application.db import get_db_connection, init_db
from application import create_app


with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )

    with app.app_context():
        init_db()
        get_db_connection().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


def test_get_close_db(app):
    with app.app_context():
        connection = get_db_connection()
        assert connection is get_db_connection()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        connection.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("application.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
