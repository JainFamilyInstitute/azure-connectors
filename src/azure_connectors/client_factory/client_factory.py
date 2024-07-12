import inspect
from typing import Any, Type

from azure_connectors.config import CredentialScope
from azure_connectors.credential import AzureCredential


def get_parameters(cls: Type[Any]) -> list[str]:
    """
    Get the list of parameters for a given class.

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


def create_azure_client_class(base_class: Type[Any], settings_class: Type[Any], scope: CredentialScope):
    

    class DynamicAzureClient(base_class):
        
        @classmethod
        def from_env(cls, *args, **kwargs):
            # find settable parameters for settings class
            
            settings_kwargs, base_kwargs = split_kwargs(settings_class, kwargs)
            credential_provider = AzureCredential.from_env(scope=scope)
            
            # any kwargs passed that apply to settings go to settings

            settings = settings_class(**settings_kwargs)
            credential = credential_provider.get_credential()

            
            return base_class(account_url=settings.account_url, credential=credential, *args, **base_kwargs)

    DynamicAzureClient.__name__ = base_class.__name__
    return DynamicAzureClient