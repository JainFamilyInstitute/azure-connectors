import inspect
from typing import Any, Type


def get_parameters(cls: Type[Any]) -> list[str]:
    """
    Get the list of parameter names for a given class.

    Args:
        cls (Type[Any]): The class to inspect.

    Returns:
        list[str]: A list of parameter names for the class.

    """
    return [x for x in inspect.signature(cls).parameters.keys() if not x.startswith('_')]


def split_kwargs(cls: Type[Any], kwargs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Splits a dicitonary of keyword arguments into two dictionaries: 
    those used in initializing the specified class, and the remainder.

    Args:
        settings_class (Type[Any])): A class.
        kwargs (dict[str, Any]): The keyword arguments to be split.

    Returns:
        tuple[dict[str, Any], dict[str, Any]]: A tuple containing two dictionaries. The first dictionary
            contains the keyword arguments that match initializer for the specified class, and the second dictionary
            contains the remaining keyword arguments.

    """

    cls_parameters = get_parameters(cls)
    cls_kwargs = {k: v for k, v in kwargs.items() if k in cls_parameters}
    remaining_kwargs = {k: v for k, v in kwargs.items() if k not in cls_parameters}
    return cls_kwargs, remaining_kwargs