# noqa: E501
# fmt: skip

import os
import re

import pytest
from pydantic import ValidationError
from utils import generate_scenarios

module_name = "azure_connectors.credential.settings"
class_name = "AzureCredentialSettings"

SCOPE_PREFIX = "AZURE_CREDENTIAL_"
SCOPE_ENV_VAR = "AZURE_CREDENTIAL_SCOPE"
SOURCE_ENV_VAR = "AZURE_CREDENTIAL_SOURCE"

# specify the environment variables to try out
env_vars = {
    SCOPE_ENV_VAR: "https://storage.azure.com/.default",
    SOURCE_ENV_VAR: "cli",
}

envfile_vars = {
    SCOPE_ENV_VAR: "https://database.windows.net/.default",
    SOURCE_ENV_VAR: "default",
}

passed_vars = {
    SOURCE_ENV_VAR: "default",
    SCOPE_ENV_VAR: "https://storage.azure.com/.default",
}

passed_param_names = {
    k: re.sub(f"{SCOPE_PREFIX}", "", k).lower() for k in passed_vars.keys()
}

unrelated_dict = {
    "UNRELATED_VAR": "unrelated_value",
}
expected_value_scenarios = (
    (assignments_dict, expected_value, (module_name, class_name))
    for assignments_dict, expected_value in generate_scenarios(
        env_vars=env_vars,
        envfile_vars=envfile_vars,
        unrelated_vars=unrelated_dict,
        passed_vars=passed_vars,
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

    expected_scope = expected_value[SCOPE_ENV_VAR]
    expected_source = expected_value[SOURCE_ENV_VAR]

    # Assert that the environment variable is read correctly
    assert settings.scope.value == expected_scope
    assert settings.source.value == expected_source


@pytest.mark.parametrize(
    "setup_env, import_class",
    [
        (
            {
                "env_vars": {},
                "envfile_vars": {},
                "excluded_vars": {SCOPE_ENV_VAR, SOURCE_ENV_VAR},
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
                "env_vars": {SCOPE_ENV_VAR: "https://storage.azure.com/.default"},
                "envfile_vars": {
                    SCOPE_ENV_VAR: "https://database.windows.net/.default",
                    SOURCE_ENV_VAR: "default",
                },
                "excluded_vars": set(),
                "unrelated_vars": {},
            },
            (module_name, class_name),
        )
    ],
    indirect=["setup_env", "import_class"],
)
def test_env_vars_override(setup_env, import_class):
    # Ensure that a ValidationError is raised when a required environment variable is missing

    settings = import_class()

    expected_scope = "https://storage.azure.com/.default"
    expected_source = "default"

    # Assert that the environment variable is read correctly and that the env_vars override the envfile_vars
    assert settings.scope.value == expected_scope
    assert settings.source.value == expected_source


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
