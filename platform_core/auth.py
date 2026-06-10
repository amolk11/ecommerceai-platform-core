import hashlib

from sqlalchemy import text


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()


def validate_api_key(connection, api_key: str) -> dict | None:

    api_key_hash = hash_api_key(api_key)

    result = (
        connection.execute(
            text(
                """
            SELECT
                ak.api_key_id,
                c.client_id,
                c.client_name,
                c.is_active
            FROM api_keys ak
            JOIN clients c
                ON ak.client_id = c.client_id
            WHERE ak.api_key_hash = :api_key_hash
            """
            ),
            {"api_key_hash": api_key_hash},
        )
        .mappings()
        .first()
    )

    if not result:
        return None

    if not result["is_active"]:
        return None

    return dict(result)
