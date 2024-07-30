import inspect
from typing import Any, Type

from .typing import ParamMap, SplitKwargs


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


def split_init_kwargs(
    kwargs: dict[str, Any],
    cls: Type[Any],
) -> SplitKwargs:
    """
    Splits a dictionary of keyword arguments into two dictionaries:
    those used in initializing a given class, and the remainder.

    Args:
        kwargs (dict[str, Any]): The keyword arguments to be split.

    Returns:
        tuple[dict[str, Any], dict[str, Any]]: A tuple containing two dictionaries. The first dictionary
            contains the keyword arguments that match the initializer for the settings class, and the second
            contains the remaining keyword arguments.

    """

    cls_parameters = get_parameters(cls)
    cls_kwargs = {k: v for k, v in kwargs.items() if k in cls_parameters}
    remaining_kwargs = {k: v for k, v in kwargs.items() if k not in cls_parameters}
    return SplitKwargs(cls_kwargs, remaining_kwargs)


def update_dict_from_object_properties(
    dict_to_update: dict[str, Any], cls: Type[Any], param_map: ParamMap
) -> dict[str, Any]:
    """
    Updates the client_kwargs dictionary with credentials obtained from
    an AzureCredential provider. Which properties of the credential to include in
    the dictionary update, and the kwarg name to use, is given by the param_map.

    Any properties of the credential that are already present in the client_kwargs
    dictionary will not be updated.

    Args:
        client_kwargs (dict[str, Any]): The client_kwargs dictionary to be updated.
        credential (TokenCredential): The Azure credential object.
        cred_param_map (CredParamMap): The mapping of credential properties to parameter names.

    Returns:
        dict[str, Any]: The updated client_kwargs dictionary.
    """

    for cls_property, param_name in param_map.items():
        if param_name not in dict_to_update.keys():
            dict_to_update.update({param_name: getattr(cls, cls_property)})

    return dict_to_update
