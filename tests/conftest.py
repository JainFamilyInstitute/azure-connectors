# tests/conftest.py
import importlib
import sys
from pathlib import Path

import pytest

ENV_FILE_ENV_VAR = "AZURE_CONNECTORS_ENV_FILE"


def reload_all_modules():
    # This function will reload all modules in the 'src' directory
    src_path = Path(__file__).resolve().parent.parent / "src"
    for module in list(sys.modules.values()):
        try:
            if (
                module
                and hasattr(module, "__file__")
                and str(module.__file__).startswith(str(src_path))
            ):
                importlib.reload(module)
        except Exception as e:
            print(f"Error reloading module {module.__name__}: {e}")


@pytest.fixture
def setup_env(monkeypatch, tmp_path, request):
    # Retrieve envfile_content and env_vars from request.param
    envfile_content = request.param.get("envfile_content", None)
    env_vars = request.param.get("env_vars", None)

    # Delete any pre-existing environment variables
    monkeypatch.delenv(ENV_FILE_ENV_VAR, raising=False)

    if env_vars:
        for var in env_vars.keys():
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

    yield

    # Clean up environment variables after the test
    if envfile_content:
        monkeypatch.delenv(ENV_FILE_ENV_VAR, raising=False)

    if env_vars:
        for var in env_vars.keys():
            monkeypatch.delenv(var, raising=False)

    reload_all_modules()
