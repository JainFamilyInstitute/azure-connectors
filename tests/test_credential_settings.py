# noqa: E501
# fmt: skip

import os

import pytest
from pydantic import ValidationError

from utils import generate_scenarios

module_name = "azure_connectors.credential.settings"
class_name = "AzureCredentialSettings"

SCOPE_ENV_VAR = "AZURE_CREDENTIAL_SCOPE"
SCOPE_ENV_VALUE = "https://storage.azure.com/.default"
SOURCE_ENV_VAR = "AZURE_CREDENTIAL_SOURCE"
SOURCE_ENV_VALUE = "cli"
SCOPE_ENVFILE_VAR = SCOPE_ENV_VAR
SCOPE_ENVFILE_VALUE ="https://database.windows.net/.default"
SOURCE_ENVFILE_VAR = SOURCE_ENV_VAR
SOURCE_ENVFILE_VALUE = "default"
UNRELATED_VAR = "UNRELATED_VAR"
UNRELATED_VALUE = "unrelated_value"

BLANK = ""

env_dict = {
    SCOPE_ENV_VAR: SCOPE_ENV_VALUE,
    SOURCE_ENV_VAR: SOURCE_ENV_VALUE,
}

envfile_dict = {
    SCOPE_ENVFILE_VAR: SCOPE_ENVFILE_VALUE,
    SOURCE_ENVFILE_VAR: SOURCE_ENVFILE_VALUE,
}

unrelated_dict = {
    UNRELATED_VAR: UNRELATED_VALUE,
}
expected_value_scenarios = ((assignments_dict, expected_value, (module_name, class_name))
                            for assignments_dict, expected_value in generate_scenarios(env_dict, envfile_dict, unrelated_dict))



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

    expected_scope = expected_value[SCOPE_ENV_VAR]
    expected_source = expected_value[SOURCE_ENV_VAR]

    # Assert that the environment variable is read correctly
    assert settings.scope.value == expected_scope
    assert settings.source.value == expected_source

@pytest.mark.parametrize(
    "setup_env, import_class",
    [({'env_vars': {}, 'envfile_vars': {}, 'excluded_vars':{SCOPE_ENV_VAR, SOURCE_ENV_VAR}, 'unrelated_vars': {}}, (module_name, class_name))],
    indirect=["setup_env", "import_class"],
)
def test_missing_env_vars(setup_env, import_class):
    # Ensure that a ValidationError is raised when a required environment variable is missing
    with pytest.raises(ValidationError):
        import_class()

# @pytest.mark.parametrize(
#     "setup_env, import_class",
#     [({'env_vars': {}, 'envfile_vars': {}, 'excluded_vars':{SCOPE_ENV_VAR, SOURCE_ENV_VAR}, 'unrelated_vars': {}}, (module_name, class_name))],
#     indirect=["setup_env", "import_class"],
# )
# def test_direct_instantiation(setup_env, import_class):
#     # Ensure that the settings can be instantiated without any environment variables
#     settings = import_class(storage_account="testaccount")
#     assert settings.storage_account == "testaccount"
#     assert settings.server == "https://testaccount.table.core.windows.net"

if __name__ == "__main__":
    pytest.main(["-sv", os.path.abspath(__file__)])
