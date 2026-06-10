from sqlalchemy import text

from platform_core.database import get_platform_engine


def validate_platform_database_connection() -> None:
    """
    Validate Platform DB connectivity.
    """

    engine = get_platform_engine()

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


def validate_required_tables() -> None:
    """
    Validate required platform tables.
    """

    required_tables = ["clients", "api_keys"]

    query = text(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = :table_name
        )
        """
    )

    engine = get_platform_engine()

    with engine.connect() as connection:
        for table_name in required_tables:
            exists = connection.execute(query, {"table_name": table_name}).scalar()

            if not exists:
                raise RuntimeError(f"Required table missing: {table_name}")


def validate_internal_client() -> None:
    """
    Validate internal CommerceAI client.
    """

    query = text(
        """
        SELECT EXISTS (
            SELECT 1
            FROM clients
            WHERE client_id = :client_id
        )
        """
    )

    engine = get_platform_engine()

    with engine.connect() as connection:
        exists = connection.execute(
            query, {"client_id": "commerceai-internal"}
        ).scalar()

    if not exists:
        raise RuntimeError("commerceai-internal client not found")


def validate_platform_infrastructure() -> None:
    """
    Run all platform startup validations.
    """

    validate_platform_database_connection()

    validate_required_tables()

    validate_internal_client()
