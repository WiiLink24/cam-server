import secrets
import string

from cam import db


def generate_unique_id(table: db.Model, column: object, size: int) -> str:
    # We need an alphanumeric string as an ID.
    # We only do 5 attempts, as it would take quite something to have this fail!
    for _ in range(5):
        # Our token size is in bytes, where we need characters.
        alphabet = string.ascii_letters + string.digits
        possible_key = "".join(secrets.choice(alphabet) for i in range(size))

        result = table.query.filter(column == possible_key).first()
        if result is None:
            return possible_key

    # It appears we've somehow failed.
    return ""
