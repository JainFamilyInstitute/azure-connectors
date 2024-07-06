from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from azure_connectors.enums import CredentialSource, CredentialScope
from azure_connectors.env_config import EnvConfig
from typing import Optional

class AzureCredentialSettings(BaseSettings):
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

    model_config = SettingsConfigDict(env_prefix=EnvConfig.CREDENTIALS_PREFIX, **EnvConfig.SETTINGS_BASE)

    @classmethod
    def from_env(cls, source: Optional[CredentialSource], scope: Optional[CredentialScope] = None) -> 'AzureCredentialSettings':
        """
        Create an instance of AzureCredentialSettings by reading the settings not passed explicitly 
        from the environment variables and .env file.
        
        Provided for consistency with dependent classes' from_env methods.

        Args:
            source (Optional[CredentialSource]): The source of the credentials. If not provided, it will be read from the environment.
            scope (Optional[CredentialScope]): The scope of the credentials. If not provided, it will be read from the environment.

        Returns:
            AzureCredentialSettings: An instance of AzureCredentialSettings with the settings loaded from the environment.

        """
        # pass along only the non-None arguments, so BaseSettings can handle the rest from the env
        pass_kwargs = {k: v for k,v in locals().items() if v is not None and k != 'cls'}
        return cls(**pass_kwargs)