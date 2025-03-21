import inspect
from typing import Any, Type, TypeVar

T = TypeVar("T")


def nice_pass(cls: Type[T], **kwargs) -> T:
    """
    Create an instance of the given class with the provided keyword arguments.

    Useful for BaseSettings classes where environment variable reading will break
    if constructor is passed None-valued arguments.

    Args:
        cls: The class to instantiate.
        **kwargs: Keyword arguments to pass to the class constructor.

    Returns:
        An instance of the given class with the provided keyword arguments.
    """
    pass_kwargs = {k: v for k, v in kwargs.items() if v is not None}
    return cls(**pass_kwargs)


def get_parameters(cls: Type[Any]) -> list[str]:
    """
    Get the list of parameter names for a given class.

    Args:
        cls (Type[Any]): The class to inspect.

    Returns:
        list[str]: A list of parameter names for the class.

    """
    return [
        x for x in inspect.signature(cls).parameters.keys() if not x.startswith("_")
    ]
