from pydantic import Field
from pydantic_settings import BaseSettings

from azure_connectors.config import (CredentialScope, EnvPrefix,
                                     get_settings_config)

from .enums import CredentialSource


class AzureCredentialSettings(BaseSettings):
    """
    Represents the settings for retrieving Azure AD / Entra ID credentials.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_CREDENTIAL_" (defined in azure_connectors.config.enums).

    Attributes:
        source (CredentialSource): The source of the credentials, either "cli" or "default".
        scope (CredentialScope): The scope of the credentials.
    """

    model_config = get_settings_config(EnvPrefix.AZURE_CREDENTIAL)

    source: CredentialSource = Field(default=None)
    scope: CredentialScope = Field(default=None)
