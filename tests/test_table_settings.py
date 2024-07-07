# noqa: E501
# fmt: skip

import os

import pytest
from pydantic import ValidationError

module_name = "azure_connectors.azure_tables.settings"
class_name = "AzureTableSettings"

ENV_VAR = "AZURE_TABLES_STORAGE_ACCOUNT"
ENV_VALUE = "testaccount"
ENVFILE_VAR = ENV_VAR
ENVFILE_VALUE = "testaccountfile"
UNRELATED_VAR = "UNRELATED_VAR"
UNRELATED_VALUE = "unrelated_value"

ENVFILE_CONTENT = f"{ENVFILE_VAR}={ENVFILE_VALUE}\n"
ENVFILE_CONTENT_WITH_UNRELATED = (ENVFILE_CONTENT + f"{UNRELATED_VAR}={UNRELATED_VALUE}\n")
BLANK = ""

expected_value_scenarios = [
    ({"envfile_content": BLANK, "env_vars": {ENV_VAR: ENV_VALUE}}, ENV_VALUE),
    ({"envfile_content": ENVFILE_CONTENT, "env_vars": {ENV_VAR: ENV_VALUE}}, ENV_VALUE),
    ({"envfile_content": BLANK, "env_vars": {ENV_VAR: ENV_VALUE, UNRELATED_VAR: UNRELATED_VALUE}}, ENV_VALUE),
    ({"envfile_content": ENVFILE_CONTENT, "env_vars": {ENV_VAR: BLANK},}, ENVFILE_VALUE),
    ({"envfile_content": ENVFILE_CONTENT_WITH_UNRELATED, "env_vars": {ENV_VAR: BLANK},}, ENVFILE_VALUE),
    ({"envfile_content": ENVFILE_CONTENT_WITH_UNRELATED, "env_vars": {ENV_VAR: ENV_VALUE},}, ENV_VALUE),
    ]

expected_value_tests = [(*x, (module_name, class_name)) for x in expected_value_scenarios]



@pytest.mark.parametrize(
    "setup_env, expected_value, import_class",
    expected_value_tests,
    indirect=["setup_env", "import_class"],
)
def test_env_vars(setup_env, expected_value, import_class):
    # Ensure that the settings correctly pick up environment variables,
    # read from .env file, and that set environment variables override anything in the .env file

    # Create settings instance
    settings = import_class()

    # Assert that the environment variable is read correctly
    assert settings.storage_account == expected_value
    assert settings.server == f"https://{expected_value}.table.core.windows.net"


if __name__ == "__main__":
    pytest.main(["-sv", os.path.abspath(__file__)])
