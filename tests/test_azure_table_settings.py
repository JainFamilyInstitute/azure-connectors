import os
import pytest
from pydantic import ValidationError
from azure_connectors.enums import EnvPrefix
from azure_connectors.utils import with_env_settings
from azure_connectors.azure_tables.settings import AzureTableSettings  # replace 'my_module' with the actual module name


def test_azure_table_settings_env_vars(monkeypatch):
    # Environment variables should override any .env settings
    # Mock environment variables
    monkeypatch.setenv("AZURE_TABLES_STORAGE_ACCOUNT", "testaccount")

    # Create settings instance
    settings = AzureTableSettings()

    # Assert that the environment variable is read correctly
    assert settings.storage_account == "testaccount"
    assert settings.server == "https://testaccount.table.core.windows.net"


# def test_azure_table_settings_no_env(monkeypatch):
#     # Ensure no environment variables are set
#     monkeypatch.delenv("AZURE_TABLES_STORAGE_ACCOUNT", raising=False)

#     # Create settings instance
#     settings = AzureTableSettings()

#     # Assert that the default value is used
#     assert settings.storage_account is None
#     assert settings.server == "https://None.table.core.windows.net"

# def test_azure_table_settings_custom_env_file(monkeypatch, tmp_path):
#     # Create a custom .env file content
#     env_content = """
#     AZURE_TABLES_STORAGE_ACCOUNT=customaccount
#     """

#     # Write the custom .env file to a temporary location
#     env_file = tmp_path / ".env.test"
#     env_file.write_text(env_content)

#     # Mock the location of the .env file
#     monkeypatch.setattr('os.environ', {})
#     monkeypatch.setenv("ENV_FILE", str(env_file))

#     # Create settings instance
#     settings = AzureTableSettings()

#     # Assert that the environment variable from the custom file is read correctly
#     assert settings.storage_account == "customaccount"
#     assert settings.server == "https://customaccount.table.core.windows.net"

# def test_azure_table_settings_no_env_vars(monkeypatch):
#     # Ensure no environment variables are set
#     monkeypatch.delenv("AZURE_TABLES_STORAGE_ACCOUNT", raising=False)

#     # Create settings instance
#     settings = AzureTableSettings()

#     # Assert that the default value is used
#     assert settings.storage_account is None
#     assert settings.server == "https://None.table.core.windows.net"

# Add more tests as needed to cover other scenarios
