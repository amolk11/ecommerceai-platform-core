from pathlib import Path
from urllib.parse import urlparse

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def create_database_if_not_exists(database_url: str) -> None:
    parsed = urlparse(database_url)

    database_name = parsed.path.lstrip("/")

    postgres_url = database_url.replace(f"/{database_name}", "/postgres")

    engine = create_engine(postgres_url, isolation_level="AUTOCOMMIT")

    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT 1
                FROM pg_database
                WHERE datname = :database_name
                """
            ),
            {"database_name": database_name},
        )

        exists = result.scalar() is not None

        if not exists:
            print(f"Creating database: {database_name}")

            connection.execute(text(f'CREATE DATABASE "{database_name}"'))

            print("Database created successfully.")

        else:
            print(f"Database already exists: {database_name}")


def run_sql_files(database_url: str) -> None:
    engine = create_engine(database_url)

    sql_directory = Path(__file__).parent.parent / "sql"

    sql_files = sorted(sql_directory.glob("*.sql"))

    if not sql_files:
        print("No SQL files found.")
        return

    with engine.begin() as connection:
        for sql_file in sql_files:
            print(f"Executing: {sql_file.name}")

            sql_content = sql_file.read_text(encoding="utf-8")

            connection.execute(text(sql_content))

    print("Bootstrap completed successfully.")


def main() -> None:
    load_dotenv()

    database_url = os.getenv("DB_URL")

    if not database_url:
        raise ValueError("DATABASE_URL not found in .env")

    create_database_if_not_exists(database_url)

    run_sql_files(database_url)


if __name__ == "__main__":
    main()
