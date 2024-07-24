# azure-connectors
Python connectors for passwordless login to Azure storage services (SQL, ADLSv2, blob, tables), suitable for local and containerized projects.

## Overview
For compatibility with Container Apps and Azure Functions, settings are passed as environment variables. For local development, create or extend a `.env` file in the project root. For deployment, ensure that the environment variables are set in the app. Example settings are in the `example_envs` folder.

No environment variables should contain secrets!

## Authentication
Authentication to Azure services is passwordless, using Entra ID (aka Azure AD). For local development, specify `AZURE_CREDENTIAL_SOURCE=cli` in the `.env` or as an environment variable. For deployment in an app service, container app, or function, speciry `AZURE_CREDENTIAL_SOURCE=default`.

## Usage

There are two main entrypoints to the library:
- a connector for Azure SQL, `AzureSqlConnection`
  - this has a property `.engine` that returns a sqlalchemy `Engine` object suitable for direct use with pandas `to_sql` methods.
- shadow constructors for Azure SDK `Client` objects.
  - These add a `.from_env()` method to create the object using relevant environment variables instead of passing creation arguments; any arguments passed to `from_env` will override environment values.
  - Once created, these are core Azure SDK objects, so any documentation or how-to guides you find that use these classes should work without modification (apart from creating with, e.g., `client = BlobServiceClient.from_env()`.
  - Currently implemented: `BlobServiceClient`, `BlobClient`, `ContainerClient`, `TableServiceClient`, and `SqlManagementClient`.  

## Examples
### Azure SQL
#### Pandas
```python
from azure_connectors import AzureSqlConnection
engine = AzureSqlConnection.from_env().engine
data_frame.to_sql(name=table_name, con=engine, if_exists="append", index=False)
```

#### Polars
TODO

### Azure Blob
```python
from azure_connectors import BlobServiceClient
service_client = BlobServiceClient.from_env()
print(list(service_client.get_containers()))
```
