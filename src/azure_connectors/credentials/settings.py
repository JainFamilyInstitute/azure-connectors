from pydantic import BaseModel, Field

from azure_connectors.enums import CredentialScope, EnvPrefix
from azure_connectors.utils import with_env_settings

from .enums import CredentialSource


@with_env_settings(env_prefix=EnvPrefix.CREDENTIALS)
class AzureCredentialSettings(BaseModel):
    """
    Represents the settings for retrieving Azure AD / Entra ID credentials.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_CREDENTIALS_" (defined in azure_connectors.enums).

    Attributes:
        source (CredentialSource): The source of the credentials, either "cli" or "default".
        scope (CredentialScope): The scope of the credentials.
    """

    source: CredentialSource = Field(default=None)
    scope: CredentialScope = Field(default=None)
