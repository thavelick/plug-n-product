from collections import namedtuple
from werkzeug.security import generate_password_hash, check_password_hash
from application import db


class UserCreationError(Exception):
    pass


class User(namedtuple("User", "id email password created_on")):
    @staticmethod
    def from_dict(record):
        return User(
            id=record["id"],
            email=record["email"],
            password=record["password"],
            created_on=record["created_on"],
        )

    @staticmethod
    def get(user_id):
        if user_id is None:
            return None

        record = (
            db.get_db_connection()
            .execute("SELECT * FROM user WHERE id = ?", (user_id,))
            .fetchone()
        )
        if record is None:
            return None

        return User.from_dict(record)

    @staticmethod
    def authenticate(email, unhashed_password):
        record = (
            db.get_db_connection()
            .execute("SELECT * FROM user WHERE email = ?", (email,))
            .fetchone()
        )
        if not record:
            return None

        user = User.from_dict(record)
        if not check_password_hash(user.password, unhashed_password):
            return None

        return user

    @staticmethod
    def create(email, password):
        if not email:
            raise UserCreationError("Email is required.")
        if not password:
            raise UserCreationError("Password is required.")
        if len(password) < 10:
            raise UserCreationError("Password must be at least 10 characters long.")

        connection = db.get_db_connection()
        try:
            connection.execute(
                "INSERT INTO user (email, password) VALUES (?, ?)",
                (email, generate_password_hash(password)),
            )
            connection.commit()
        except connection.IntegrityError as error:
            raise UserCreationError(
                "Sorry that account is already registered. Please sign in."
            ) from error
