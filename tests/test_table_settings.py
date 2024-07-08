# noqa: E501
# fmt: skip

import os

import pytest
from pydantic import ValidationError
from utils import generate_scenarios

module_name = "azure_connectors.azure_tables.settings"
class_name = "AzureTableSettings"

ENV_DICT = {"AZURE_TABLES_STORAGE_ACCOUNT": "testaccount"}
ENVFILE_DICT = {"AZURE_TABLES_STORAGE_ACCOUNT": "testaccountfile"}
UNRELATED_DICT = {"UNRELATED_VAR" : "unrelated_value"}

expected_value_scenarios = ((assignments_dict, expected_value, (module_name, class_name))
                            for assignments_dict, expected_value in generate_scenarios(ENV_DICT, ENVFILE_DICT, UNRELATED_DICT))



@pytest.mark.parametrize(
    "setup_env, expected_value, import_class",
    expected_value_scenarios,
    indirect=["setup_env", "import_class"],
)
def test_scenarios(setup_env, expected_value, import_class):
    # Ensure that the settings correctly pick up environment variables,
    # read from .env file, and that set environment variables override anything in the .env file

    # Create settings instance
    settings = import_class()

    expected_storage_account = expected_value["AZURE_TABLES_STORAGE_ACCOUNT"]

    # Assert that the environment variable is read correctly
    assert settings.storage_account == expected_storage_account
    assert settings.server == f"https://{expected_storage_account}.table.core.windows.net"

@pytest.mark.parametrize(
    "setup_env, import_class",
    [({'env_vars': {}, 'envfile_vars': {}, 'excluded_vars':{"AZURE_TABLES_STORAGE_ACCOUNT"}, 'unrelated_vars': {}}, (module_name, class_name))],
    indirect=["setup_env", "import_class"],
)
def test_missing_env_vars(setup_env, import_class):
    # Ensure that a ValidationError is raised when a required environment variable is missing
    with pytest.raises(ValidationError):
        import_class()

@pytest.mark.parametrize(
    "setup_env, import_class",
    [({'env_vars': {}, 'envfile_vars': {}, 'excluded_vars':{"AZURE_TABLES_STORAGE_ACCOUNT"}, 'unrelated_vars': {}}, (module_name, class_name))],
    indirect=["setup_env", "import_class"],
)
def test_direct_instantiation(setup_env, import_class):
    # Ensure that the settings can be instantiated without any environment variables
    settings = import_class(storage_account="testaccount")
    assert settings.storage_account == "testaccount"
    assert settings.server == "https://testaccount.table.core.windows.net"

if __name__ == "__main__":
    pytest.main(["-sv", os.path.abspath(__file__)])
