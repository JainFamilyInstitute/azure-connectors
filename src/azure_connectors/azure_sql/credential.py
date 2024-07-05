import struct
from dataclasses import dataclass, field
from functools import cached_property
from typing import Literal, Union

from azure.identity import AzureCliCredential, DefaultAzureCredential
from pydantic import SecretBytes

BaseCredential = Union[DefaultAzureCredential, AzureCliCredential]
CredentialType = Literal["cli", "default"]


@dataclass(frozen=True)
class AzureSqlCredential:
    """
    Retrieves and stores a credential for accessing Azure SQL databases.

    Attributes:
        credential_type (CredentialType): The type of credential to use.
        scope (str): The scope of the credential.
        token (SecretBytes): Azure AD / Entra ID token for the credential.
        _base_credential (BaseCredential): The underlying Azure credential.

    Raises:
        ValueError: If an invalid value is provided for credential type.
        RuntimeError: If failed to obtain an Azure AD / Entra ID token.
    """

    credential_type: CredentialType
    scope: str = "https://database.windows.net/.default"
    _base_credential: BaseCredential = field(init=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, "_base_credential", self._get_azure_credential())

    def _get_azure_credential(self) -> BaseCredential:
        """
        Retrieves the appropriate Azure credential based on the self.credential_type.

        Returns:
            BaseCredential: The Azure credential object.

        Raises:
            ValueError: If self.credential_type invalid.
        """
        match self.credential_type:
            case "cli":
                credential = AzureCliCredential()
            case "default":
                credential = DefaultAzureCredential()
            case _:
                raise ValueError("Invalid value for credential_type.")

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
            token_bytes = credential.get_token(self.scope).token.encode("UTF-16-LE")
            token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)
            return SecretBytes(token_struct)

        except Exception as e:
            raise RuntimeError("Failed to obtain Azure AD / Entra ID token") from e
