import pytest
from pydantic import TypeAdapter, ValidationError

from azure_connectors.validation import StorageAccountName


def test_storage_account_name():
    ta = TypeAdapter(StorageAccountName)
    assert ta.validate_strings("validaccount")
    with pytest.raises(ValidationError):
        ta.validate_strings("InvalidAccount")
    with pytest.raises(ValidationError):
        ta.validate_strings("too-short")
    with pytest.raises(ValidationError):
        ta.validate_strings("thisnameiswaytoolongtobevalid")
