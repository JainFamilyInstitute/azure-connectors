import os
import re

import pytest
from pydantic import ValidationError
from utils import generate_scenarios

module_name = "azure_connectors.azure_tables.settings"
class_name = "AzureTableSettings"

SCOPE_PREFIX = "AZURE_TABLES_"

env_vars = {"AZURE_TABLES_STORAGE_ACCOUNT": "testaccount"}
envfile_vars = {"AZURE_TABLES_STORAGE_ACCOUNT": "testaccountfile"}
unrelated_vars = {"UNRELATED_VAR": "unrelated_value"}
passed_vars = {"AZURE_TABLES_STORAGE_ACCOUNT": "testaccountpassed"}
passed_param_names = {
    k: re.sub(f"{SCOPE_PREFIX}", "", k).lower() for k in passed_vars.keys()
}

expected_value_scenarios = (
    (assignments_dict, expected_value, (module_name, class_name))
    for assignments_dict, expected_value in generate_scenarios(
        env_vars=env_vars, envfile_vars=envfile_vars, unrelated_vars=unrelated_vars
    )
)


@pytest.mark.parametrize(
    "setup_env, expected_value, import_class",
    expected_value_scenarios,
    indirect=["setup_env", "import_class"],
)
def test_scenarios(setup_env, expected_value, import_class):
    # Ensure that the settings correctly pick up environment variables,
    # read from .env file, and handle passed variables

    passed_vars = dict(setup_env)  # yielded from fixture
    # Create settings instance

    kwargs = {passed_param_names[k]: v for k, v in passed_vars.items()}
    settings = import_class(**kwargs)

    expected_storage_account = expected_value["AZURE_TABLES_STORAGE_ACCOUNT"]

    # Assert that the environment variable is read correctly
    assert settings.storage_account == expected_storage_account
    assert (
        settings.server == f"https://{expected_storage_account}.table.core.windows.net"
    )


@pytest.mark.parametrize(
    "setup_env, import_class",
    [
        (
            {
                "env_vars": {},
                "envfile_vars": {},
                "excluded_vars": {"AZURE_TABLES_STORAGE_ACCOUNT"},
                "unrelated_vars": {},
            },
            (module_name, class_name),
        )
    ],
    indirect=["setup_env", "import_class"],
)
def test_missing_env_vars(setup_env, import_class):
    # Ensure that a ValidationError is raised when a required environment variable is missing
    with pytest.raises(ValidationError):
        import_class()


@pytest.mark.parametrize(
    "setup_env, import_class",
    [
        (
            {
                "env_vars": {},
                "envfile_vars": {},
                "excluded_vars": {"AZURE_TABLES_STORAGE_ACCOUNT"},
                "unrelated_vars": {},
            },
            (module_name, class_name),
        )
    ],
    indirect=["setup_env", "import_class"],
)
def test_direct_instantiation(setup_env, import_class):
    # Ensure that the settings can be instantiated without any environment variables
    settings = import_class(storage_account="testaccount")
    assert settings.storage_account == "testaccount"
    assert settings.server == "https://testaccount.table.core.windows.net"


@pytest.mark.parametrize(
    "setup_env, import_class",
    [
        (
            {
                "env_vars": {},
                "envfile_vars": {},
                "excluded_vars": {"AZURE_TABLES_STORAGE_ACCOUNT"},
                "unrelated_vars": {},
            },
            (module_name, class_name),
        )
    ],
    indirect=["setup_env", "import_class"],
)
def test_direct_bad_instantiation(setup_env, import_class):
    # Ensure that a ValidationError is raised when a required parameter is missing

    with pytest.raises(ValidationError):
        import_class(storage_account="Bad-Storage-Account-Name!")


if __name__ == "__main__":
    pytest.main(["-sv", os.path.abspath(__file__)])
