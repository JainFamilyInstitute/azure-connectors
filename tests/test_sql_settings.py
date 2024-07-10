# noqa: E501
# fmt: skip

import os
import re

import pytest
from pydantic import ValidationError
from utils import generate_scenarios

module_name = "azure_connectors.azure_sql.settings"
class_name = "AzureSqlSettings"

SCOPE_PREFIX = "AZURE_SQL_"
SERVER_ENV_VAR = "AZURE_SQL_SERVER"
DATABASE_ENV_VAR = "AZURE_SQL_DATABASE"
DRIVER_ENV_VAR = "AZURE_SQL_DRIVER"

# specify the environment variables to try out
env_vars = {
    SERVER_ENV_VAR: "testserver.database.windows.net",
    DATABASE_ENV_VAR: "testdb",
    DRIVER_ENV_VAR: "ODBC Driver ENV",
}

envfile_vars = {
    SERVER_ENV_VAR: "testserverfile.database.windows.net",
    DATABASE_ENV_VAR: "testdbfile",
    DRIVER_ENV_VAR: "ODBC Driver File",
}

passed_vars = {
    SERVER_ENV_VAR: "testserverpassed.database.windows.net",
    DATABASE_ENV_VAR: "testdbpassed",
    DRIVER_ENV_VAR: "ODBC Driver Passed",

}

passed_param_names = {k: re.sub(f"{SCOPE_PREFIX}", "", k).lower() for k in passed_vars.keys()}

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

    passed_vars = dict(setup_env) # yielded from fixture
    # Create settings instance
    
    kwargs = {passed_param_names[k]: v for k, v in passed_vars.items()}
    settings = import_class(**kwargs)

    # Check the settings members against the expected values
    assert settings.server == expected_value[SERVER_ENV_VAR]
    assert settings.database == expected_value[DATABASE_ENV_VAR]
    assert settings.driver == expected_value[DRIVER_ENV_VAR]
    assert settings.connection_string == f"DRIVER={expected_value[DRIVER_ENV_VAR]};SERVER={expected_value[SERVER_ENV_VAR]};DATABASE={expected_value[DATABASE_ENV_VAR]};"



@pytest.mark.parametrize(
    "setup_env, import_class",
    [
        (
            {
                "env_vars": {},
                "envfile_vars": {},
                "excluded_vars": {SERVER_ENV_VAR, DATABASE_ENV_VAR, DRIVER_ENV_VAR},
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
                "env_vars": env_vars, 
                "envfile_vars": envfile_vars, 
                "excluded_vars": set(),
                "unrelated_vars": {},
            },
            (module_name, class_name),
        )
    ],
    indirect=["setup_env", "import_class"],
)
def test_env_vars_override(setup_env, import_class):

    settings = import_class()

    # Check the settings members against the expected values
    assert settings.server == env_vars[SERVER_ENV_VAR]
    assert settings.database == env_vars[DATABASE_ENV_VAR]
    assert settings.driver == env_vars[DRIVER_ENV_VAR]



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
