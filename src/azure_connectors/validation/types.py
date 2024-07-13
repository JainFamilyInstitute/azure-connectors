from pydantic import AfterValidator
from typing_extensions import Annotated

from azure_connectors.validation.validators import (
    validate_azure_sql_server_address,
    validate_storage_account_name,
)

StorageAccountName = Annotated[str, AfterValidator(validate_storage_account_name)]
AzureSqlServerDomainName = Annotated[
    str, AfterValidator(validate_azure_sql_server_address)
]
