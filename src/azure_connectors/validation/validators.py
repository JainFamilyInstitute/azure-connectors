import re


def validate_storage_account_name(v: str) -> str:
    if not re.match(r"^[a-z0-9]{3,24}$", v):
        raise ValueError(
            "Storage account name must be between 3 and 24 characters long and can only contain lowercase letters and numbers."
        )
    if not re.match(r"^[a-z0-9]", v):
        raise ValueError("Storage account name must start with a letter or a number.")
    return v


def validate_azure_sql_server_address(v: str) -> str:
    if not v.lower().endswith(".database.windows.net"):
        raise ValueError(
            "Server must be a valid Azure SQL server address ending with '.database.windows.net'."
        )

    # Ensure the rest of the address (excluding the domain) is valid
    server_name = v.split(".")[0]
    if not (3 <= len(server_name) <= 63):
        raise ValueError("Server name must be between 3 and 63 characters long.")
    if not server_name[0].isalpha():
        raise ValueError("Server name must start with a letter.")
    if not all(c.isalnum() or c == "-" for c in server_name):
        raise ValueError("Server name can only contain letters, numbers, and hyphens.")
    if "--" in server_name:
        raise ValueError("Server name cannot contain consecutive hyphens.")
    if not server_name[-1].isalnum():
        raise ValueError("Server name must end with a letter or a number.")

    return v.lower()


def validate_azure_sql_database_name(v: str) -> str:
    if not v:
        raise ValueError("Database name must not be empty.")
    if len(v) > 128:
        raise ValueError("Database name must be 128 characters or fewer.")
    if not v[0].isalpha():
        raise ValueError("Database name start with an alphabetic character.")
    if " " in v:
        raise ValueError("Database name must not contain spaces.")
    if re.search(r'[\\/\:*?"<>|]', v):
        raise ValueError("Database name contains invalid characters.")
    return v
