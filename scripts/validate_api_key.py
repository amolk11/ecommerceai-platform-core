import hashlib
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()


def main() -> None:

    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/validate_api_key.py <api_key>"
        )
        sys.exit(1)

    api_key = sys.argv[1]

    load_dotenv()

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL not found")

    api_key_hash = hash_api_key(api_key)

    engine = create_engine(database_url)

    with engine.connect() as connection:

        result = connection.execute(
            text(
                """
                SELECT
                    api_key_id,
                    client_id,
                    is_active
                FROM api_keys
                WHERE api_key_hash = :api_key_hash
                """
            ),
            {"api_key_hash": api_key_hash},
        ).mappings().first()

        if not result:
            print("INVALID API KEY")
            return

        if not result["is_active"]:
            print("API KEY IS DISABLED")
            return

        print()
        print("API KEY VALID")
        print("-" * 40)
        print(f"Client ID : {result['client_id']}")
        print(f"API Key ID: {result['api_key_id']}")
        print()


if __name__ == "__main__":
    main()
    