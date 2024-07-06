from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from azure_connectors.credentials.types import CredentialSource, CredentialScope
from typing import Optional

class AzureCredentialSettings(BaseSettings):
    """
    Represents the settings for retrieving Azure AD / Entra ID credentials.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_CREDENTIALS_".

    Attributes:
        source (CredentialSource): The source of the credentials, either "cli" or "default".
        scope (CredentialScope): The scope of the credentials.
    """

    source: CredentialSource = Field(default=None)
    scope: CredentialScope = Field(default=None)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AZURE_CREDENTIALS_",  # field env vars are prefixed with "AZURE_SQL_"
        extra="ignore",  # don't throw error for unrelated items in .env
        hide_input_in_errors=True,  # don't display any secrets in .env on ValidationError
    )

    @classmethod
    def from_env(cls, source: Optional[CredentialSource], scope: Optional[CredentialScope] = None) -> 'AzureCredentialSettings':
        """
        Create an instance of AzureCredentialSettings by reading the settings not passed explicitly
          from the environment variables and .env file.
        Provided for consistency with dependent classes' from_env methods.

        Returns:
            AzureCredentialSettings: An instance of AzureCredentialSettings with the settings loaded from the environment.

        """
        pass_kwargs = {k: v for k,v in locals().items() if v is not None and k != 'cls'}
        return cls(**pass_kwargs)