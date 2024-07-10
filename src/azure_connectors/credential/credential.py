import struct
from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional

from azure.identity import AzureCliCredential, DefaultAzureCredential
from pydantic import SecretBytes

from azure_connectors.config.enums import CredentialScope
from azure_connectors.credential.settings import AzureCredentialSettings
from azure_connectors.credential.types import BaseCredential

from .enums import CredentialSource


@dataclass(frozen=True)
class AzureCredential:
    """
    Retrieves and stores a credential for accessing Azure SQL databases.

    Attributes:
        settings (AzureCredentialSettings): The settings for the Azure credentials.
        token (SecretBytes): Azure AD / Entra ID token for the credential.

    Raises:
        ValueError: If an invalid value is provided for credential type.
        RuntimeError: If failed to obtain an Azure AD / Entra ID token.
    """

    settings: AzureCredentialSettings
    _base_credential: BaseCredential = field(init=False, repr=False)

    @classmethod
    def from_env(
        cls,
        source: Optional[CredentialSource] = None,
        scope: Optional[CredentialScope] = None,
    ) -> "AzureCredential":
        """
        Creates an instance of `AzureCredentials` by reading settings not explicitly passed from
        environment variables and the .env file.

        Args:
            source (Optional[CredentialSource]): The source of the credentials. If not provided, it will be read from the environment.
            scope (Optional[CredentialScope]): The scope of the credentials. If not provided, it will be read from the environment.

        Returns:
            AzureCredential: An instance of `AzureCredential` initialized with the settings from environment variables.
        """

        # pass along only the non-None arguments, so Settings can handle the rest from the env
        pass_args = {k: v for k, v in locals().items() if v is not None and k != "cls"}

        settings = AzureCredentialSettings(**pass_args)

        return cls(settings=settings)

    def __post_init__(self):
        object.__setattr__(self, "_base_credential", self._get_azure_credential())

    def _get_azure_credential(self) -> BaseCredential:
        """
        Retrieves the appropriate Azure credential based on the self.credential_type.

        Returns:
            BaseCredential: The Azure credential object.

        Raises:
            ValueError: If self.settings.source isn't a valid value.
        """

        credential: BaseCredential

        match self.settings.source:
            case CredentialSource.CLI:
                credential = AzureCliCredential()
            case CredentialSource.DEFAULT:
                credential = DefaultAzureCredential()
            case _:
                raise ValueError("Invalid value for credential source.")

        return credential

    @cached_property
    def token(self) -> SecretBytes:
        """
        Retrieves the Azure AD / Entra ID token.

        Returns:
            SecretBytes: The token as a SecretBytes object.

        Raises:
            RuntimeError: If failed to obtain the token.
        """
        try:
            credential = self._base_credential
            token_bytes = credential.get_token(
                str(self.settings.scope.value)
            ).token.encode("UTF-16-LE")
            token_struct = struct.pack(
                f"<I{len(token_bytes)}s", len(token_bytes), token_bytes
            )
            return SecretBytes(token_struct)

        except Exception as e:
            raise RuntimeError("Failed to obtain Azure AD / Entra ID token") from e


    def get_credential(self) -> BaseCredential:
        return self._base_credential