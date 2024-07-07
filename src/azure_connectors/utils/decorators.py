from typing import Callable, Type, TypeVar, cast

from pydantic import BaseModel
from pydantic.config import ExtraValues
from pydantic_settings import BaseSettings, SettingsConfigDict

from azure_connectors.constants import ENV_FILE
from azure_connectors.enums import EnvPrefix

T = TypeVar('T', bound=BaseModel)

def with_env_settings(
    env_prefix: EnvPrefix,
    env_file: str = ENV_FILE,
    extra: ExtraValues = "ignore",
    hide_input_in_errors: bool = True,
    **kwargs,
) -> Callable[[Type[T]], Type[T]]:
    """
    Factory decorator that subclasses pydantic_settings.BaseSettings and adds model configuration settings 
    to leverage pydantic_settings' environment variable handling.

    NB: This roundabout way of creating a class (rather than using a factory for model_config) is necessary
        because pydantic_settings requires the model_config to be set at time of class definition.

    Args:
        env_prefix (str): The prefix to use when reading environment variables for the model configuration.
        env_file (str, optional): The name of the environment file to load. Defaults to ".env".
        extra (ExtraValues, optional): The behavior for handling extra values in the environment. Defaults to "ignore".
        hide_input_in_errors (bool, optional): Whether to hide input values in error messages. Defaults to True.
        **kwargs: Additional keyword arguments to pass to the model configuration.

    Returns:
        function: A decorator function that adds model configuration settings to a class.

    Example:
        @with_model_config(env_prefix="AZURE_MAGIC_")
        class AzureMagicSettings(BaseSettings):
            # class definition
    """

    def decorator(cls: Type[T]) -> Type[T]:

        if issubclass(cls, BaseSettings):
            raise ValueError(
                f"Cannot decorate a class that is already a subclass of BaseSettings: {cls}"
            )

        model_config = SettingsConfigDict(
            env_file=env_file,
            env_prefix=env_prefix.value,
            extra=extra,
            hide_input_in_errors=hide_input_in_errors,
            **kwargs, # type: ignore
        )

        new_cls = type(
            cls.__name__, (BaseSettings, cls), {"model_config": model_config}
        )

        return cast(Type[T], new_cls)

    return decorator
