import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine

from platform_core.auth import validate_api_key


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_api_key.py <api_key>")
        sys.exit(1)

    api_key = sys.argv[1]

    load_dotenv()

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL not found")

    engine = create_engine(database_url)

    with engine.connect() as connection:

        result = validate_api_key(connection, api_key)

        if not result:
            print("INVALID API KEY")
            return

        print()
        print("API KEY VALID")
        print("-" * 40)
        print(f"Client ID : {result['client_id']}")
        print(f"API Key ID: {result['api_key_id']}")
        print()


if __name__ == "__main__":
    main()
    