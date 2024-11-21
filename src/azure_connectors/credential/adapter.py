from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .credential import AzureCredential


@dataclass(frozen=True)
class BaseCredentialAdapter(ABC):
    """
    Interface for credential adapters.
    Credential adapters are used to translate AzureCredential properties into
    appropriate keyword arguments for Azure SDK client classes via a model_dump
    method (for consistency with pydantic_settings).
    """

    credential: AzureCredential

    @abstractmethod
    def model_dump(self) -> dict[str, Any]:
        pass


@dataclass(frozen=True)
class CredentialAdapter(BaseCredentialAdapter):
    """
    Credential adapter for most Azure SDK client classes.
    Credential properties are translated into keyword arguments for client classes
    via a model_dump method (for consistency with pydantic_settings).

    Attributes:
        credential (AzureCredential): The Azure credential to use.
    """

    def model_dump(self) -> dict[str, Any]:
        """
        Generate a dictionary of keyword arguments from the credential properties.

        Returns:
            dict[str, Any]: A dictionary of keyword arguments.
        """

        return dict(credential=self.credential.base_credential)


@dataclass(frozen=True)
class SqlCredentialAdapter(BaseCredentialAdapter):
    """
    Credential adapter for Azure SQL client classes.
    Credential adapters are used to translate AzureCredential properties into
    appropriate keyword arguments for Azure SDK client classes via a model_dump
    method (for consistency with pydantic_settings).
    """

    credential: AzureCredential

    def model_dump(self) -> dict[str, Any]:
        """
        Generate a dictionary of keyword arguments from the credential properties.

        Returns:
            dict[str, Any]: A dictionary of keyword arguments.
        """

        return dict(
            credential=self.credential.base_credential,
            subscription_id=self.credential.subscription_id,
        )
