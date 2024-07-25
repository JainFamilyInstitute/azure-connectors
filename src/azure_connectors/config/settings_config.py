from typing import Any

from pydantic.config import ExtraValues
from pydantic_settings import SettingsConfigDict
from pydantic_settings.sources import DotenvType

from .enums import EnvPrefix
from .env_file import ENV_FILE


def get_settings_config(
    env_prefix: EnvPrefix,
    *,
    env_file: DotenvType = ENV_FILE,
    extra: ExtraValues = "ignore",
    hide_input_in_errors: bool = True,
    frozen: bool = True,
    **kwargs: Any,
) -> SettingsConfigDict:
    return SettingsConfigDict(
        env_prefix=env_prefix.value,
        env_file=env_file,
        extra=extra,
        hide_input_in_errors=hide_input_in_errors,
        frozen=frozen,
        **kwargs,
    )
