# tests/conftest.py
import importlib

import pytest
from utils import EnvDict, EnvSet, create_envfile_content, reload_all_modules

ENV_FILE_ENV_VAR = "AZURE_CONNECTORS_ENV_FILE"


@pytest.fixture
def setup_env(monkeypatch, tmp_path, request):
    # Retrieve envfile_vars and env_vars from request.param
    env_vars: EnvDict = request.param.get("env_vars", dict())
    envfile_vars: EnvDict = request.param.get("envfile_vars", dict())
    excluded_vars: EnvSet = request.param.get("excluded_vars", set())
    passed_vars: EnvDict = request.param.get("passed_vars", dict())
    all_vars = env_vars.keys() | envfile_vars.keys() | excluded_vars

    envfile_content = create_envfile_content(envfile_vars)

    # Delete any pre-existing environment variables
    monkeypatch.delenv(ENV_FILE_ENV_VAR, raising=False)

    if all_vars:
        for var in all_vars:
            monkeypatch.delenv(var, raising=False)

    # Create a temporary .env file

    temp_env_file = tmp_path / ".env"
    temp_env_file.write_text(envfile_content)

    # Set the environment variable to point to the temporary .env file
    monkeypatch.setenv(ENV_FILE_ENV_VAR, str(temp_env_file))
    print(f"temporary_env_file: {str(temp_env_file)}")  # Debug print statement

    # Set environment variables if env_vars is provided
    if env_vars:
        for var, value in env_vars.items():
            if value is not None and value != "":
                monkeypatch.setenv(var, value)

    # Reload all modules in the 'src' directory to ensure they pick up the new environment variables
    reload_all_modules()

    yield passed_vars

    # Clean up environment variables after the test
    if envfile_content:
        monkeypatch.delenv(ENV_FILE_ENV_VAR, raising=False)

    if all_vars:
        for var in all_vars:
            monkeypatch.delenv(var, raising=False)

    reload_all_modules()


@pytest.fixture
def import_class(request):
    module_name, class_name = request.param
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
