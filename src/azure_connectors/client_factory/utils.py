from typing import Any, Type

from azure_connectors.utils import split_init_kwargs

from .typing import ClientSettings


def get_client_kwargs(
    kwargs: dict[str, Any], settings_class: Type[ClientSettings]
) -> dict[str, Any]:
    """
    Logic for sensible handling of passed keyword arguments for from_env:
        - any keyword arguments that match Settings class properties are passed to the settings class.
        - Settings class is initialized with those properties and used to generate client settings.
        - Remaining keyword arguments are treated as client settings arguments; if they match any keywords from
          settings generated by the Settings class, they override the generated settings.

    Args:
        kwargs: Passed keyword arguments for from_env.
        settings_class: The settings class to use for generating client keyword arguments.

    Returns:
        dict[str, Any]: The keyword arguments to pass on to the client class constructor.
    """
    settings_kwargs, base_kwargs = split_init_kwargs(kwargs, settings_class)
    settings = settings_class(**settings_kwargs)
    client_kwargs = settings.model_dump()
    client_kwargs.update(base_kwargs)

    return client_kwargs
