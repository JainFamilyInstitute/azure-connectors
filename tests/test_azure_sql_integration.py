import pytest
from loguru import logger
from pydantic import SecretBytes
from sqlalchemy import text
from sqlalchemy.exc import OperationalError


@pytest.mark.integration
def test_sql_connection_authentication(monkeypatch):
    from azure_connectors import AzureSqlConnection

    try:
        # Attempt to create an instance of SQLInfo from environment variables
        logger.info("Creating SQLInfo instance from environment variables")
        sql_info = AzureSqlConnection.from_env()

        # Check if the token is obtained correctly
        logger.info("Obtaining Azure AD token")
        token = sql_info.credential.token
        assert token is not None, "Failed to obtain Azure AD token"
        logger.info("Token obtained successfully")
        assert isinstance(token, SecretBytes)

        # Attempt to create a SQLAlchemy engine and connect to the database
        logger.info("Creating SQLAlchemy engine")
        engine = sql_info.default_engine
        logger.info("Connecting to the database")
        with engine.connect() as connection:
            logger.info("Executing test query")
            result = connection.execute(
                text(
                    "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
                )
            )
            logger.debug(result)
            assert result, "Failed to execute test query"
        logger.info("Test query executed successfully")

    except (ValueError, OperationalError) as e:
        logger.error(
            f"Test failed with error: {e}. Please ensure you have a valid .env file or environment variables."
        )
        pytest.fail(f"Test failed with error: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
