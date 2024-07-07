import os

import pytest
from pydantic import ValidationError

ENV_VAR = "AZURE_TABLES_STORAGE_ACCOUNT"
ENV_VALUE = "testaccount"
ENVFILE_VAR = ENV_VAR
ENVFILE_VALUE = "testaccountfile"
UNRELATED_VAR = "UNRELATED_VAR"
UNRELATED_VALUE = "unrelated_value"

ENV_FILE_CONTENT = f"{ENVFILE_VAR}={ENVFILE_VALUE}\n"
ENV_FILE_CONTENT_WITH_UNRELATED = (
    ENV_FILE_CONTENT + f"{UNRELATED_VAR}={UNRELATED_VALUE}\n"
)
BLANK = ""


@pytest.mark.parametrize(
    "setup_env",
    [
        {"envfile_content": BLANK, "env_vars": {ENV_VAR: ENV_VALUE}},
        {"envfile_content": ENV_FILE_CONTENT, "env_vars": {ENV_VAR: ENV_VALUE}},
    ],
    indirect=True,
)
def test_azure_table_settings_env_vars(setup_env):
    # Ensure that the settings correctly pick up environment variables,
    # and that the environment variables override anything in the .env file
    from azure_connectors.azure_tables.settings import AzureTableSettings

    # Create settings instance
    settings = AzureTableSettings()

    # Assert that the environment variable is read correctly
    assert settings.storage_account == ENV_VALUE
    assert settings.server == f"https://{ENV_VALUE}.table.core.windows.net"


@pytest.mark.parametrize(
    "setup_env",
    [
        {
            "envfile_content": BLANK,
            "env_vars": {ENV_VAR: ENV_VALUE, UNRELATED_VAR: UNRELATED_VALUE},
        },
    ],
    indirect=True,
)
def test_azure_table_settings_unrelated_env_vars(setup_env):
    # Ensure that the settings ignore unrelated env vars
    from azure_connectors.azure_tables.settings import AzureTableSettings

    # Create settings instance
    settings = AzureTableSettings()

    # Assert that the environment variable is read correctly
    assert settings.storage_account == ENV_VALUE
    assert settings.server == f"https://{ENV_VALUE}.table.core.windows.net"

    with pytest.raises(AttributeError):
        assert settings.unrelated_var == UNRELATED_VALUE


@pytest.mark.parametrize(
    "setup_env",
    [
        {
            "envfile_content": ENV_FILE_CONTENT,
            "env_vars": {ENV_VAR: BLANK},
        },
        {
            "envfile_content": ENV_FILE_CONTENT_WITH_UNRELATED,
            "env_vars": {ENV_VAR: BLANK},
        },
    ],
    indirect=True,
)
def test_azure_table_settings_env_file(setup_env):
    # Ensure that the settings correctly pick up environment variables from the .env file

    from azure_connectors.azure_tables.settings import AzureTableSettings

    # Create settings instance
    settings = AzureTableSettings()

    # Assert that the environment variable is read correctly
    assert settings.storage_account == ENVFILE_VALUE
    assert settings.server == f"https://{ENVFILE_VALUE}.table.core.windows.net"


@pytest.mark.parametrize(
    "setup_env",
    [
        {
            "envfile_content": ENV_FILE_CONTENT_WITH_UNRELATED,
            "env_vars": {ENV_VAR: BLANK},
        }
    ],
    indirect=True,
)
def test_azure_table_settings_env_file_with_unrelated(setup_env):
    # Ensure that the settings correctly pick up environment variables from the .env file
    # when there are unrelated environment variables

    from azure_connectors.azure_tables.settings import AzureTableSettings

    # Create settings instance
    settings = AzureTableSettings()

    # Assert that the environment variable is read correctly
    assert settings.storage_account == ENVFILE_VALUE
    assert settings.server == f"https://{ENVFILE_VALUE}.table.core.windows.net"

    with pytest.raises(AttributeError):
        assert settings.unrelated_var == UNRELATED_VALUE


@pytest.mark.parametrize(
    "setup_env",
    [{"envfile_content": BLANK, "env_vars": {ENV_VAR: BLANK}}],
    indirect=True,
)
def test_azure_table_settings_no_env(setup_env, monkeypatch):
    from azure_connectors.azure_tables.settings import AzureTableSettings

    # Create settings instance and expect a ValidationError
    with pytest.raises(ValidationError):
        AzureTableSettings()


if __name__ == "__main__":
    pytest.main(["-sv", os.path.abspath(__file__)])
