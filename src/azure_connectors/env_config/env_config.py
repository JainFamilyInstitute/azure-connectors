class EnvConfig:
    """
    Container class for the pydantic_settings model_config used in *Settings classes.
    Add prefixes for environment variables to this file if implementing a new connector.

    """

    ENV_FILE: str = ".env"
    AZURE_SQL_PREFIX: str = "AZURE_SQL_"
    AZURE_TABLES_PREFIX: str = "AZURE_TABLES_"
    CREDENTIALS_PREFIX: str = "AZURE_CREDENTIALS_"

    SETTINGS_BASE = {
        "env_file": ENV_FILE,  # Read any settings not defined as environment variables from ENV_FILE
        "extra": "ignore",  # Don't throw error for unrelated items in .env
        "hide_input_in_errors": True,  # Don't display any secrets in .env on ValidationError
    }

    def __new__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__name__} is not meant to be instantiated. Usage: {cls.__name__}.ENV_FILE."
        )
