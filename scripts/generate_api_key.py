import hashlib
import os
import secrets
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from platform_core.auth import hash_api_key


def generate_api_key() -> str:
    return f"cai_sk_{secrets.token_urlsafe(32)}"


def get_next_api_key_id(connection) -> str:
    result = connection.execute(
        text(
            """
            SELECT COUNT(*)
            FROM api_keys
            """
        )
    )

    count = result.scalar()

    return f"ak_{count + 1:06d}"


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: python scripts/generate_api_key.py <client_id>")
        sys.exit(1)

    client_id = sys.argv[1]

    load_dotenv()

    database_url = os.getenv("DB_URL")

    if not database_url:
        raise ValueError("DB_URL not found")

    engine = create_engine(database_url)

    with engine.begin() as connection:

        client_exists = connection.execute(
            text(
                """
                SELECT 1
                FROM clients
                WHERE client_id = :client_id
                """
            ),
            {"client_id": client_id},
        ).scalar()

        if not client_exists:
            raise ValueError(f"Client '{client_id}' does not exist.")

        api_key = generate_api_key()

        api_key_hash = hash_api_key(api_key)

        api_key_id = get_next_api_key_id(connection)

        connection.execute(
            text(
                """
                INSERT INTO api_keys (
                    api_key_id,
                    client_id,
                    api_key_hash
                )
                VALUES (
                    :api_key_id,
                    :client_id,
                    :api_key_hash
                )
                """
            ),
            {
                "api_key_id": api_key_id,
                "client_id": client_id,
                "api_key_hash": api_key_hash,
            },
        )

    print()
    print("API Key Created Successfully")
    print("-" * 40)
    print(f"Client ID : {client_id}")
    print(f"API Key ID: {api_key_id}")
    print()
    print("SAVE THIS KEY NOW")
    print()
    print(api_key)
    print()


if __name__ == "__main__":
    main()
    