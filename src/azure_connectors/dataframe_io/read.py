from typing import Any, Literal
from azure_connectors import AzureSqlConnection
import sqlalchemy
import polars as pl


def read_df(
    query: str,
    iter_batches: Literal[False] = False,
    batch_size: int | None = None,
    schema_overrides: pl.Schema | None = None,
    infer_schema_length: int | None = None,
    execute_options: dict[str, Any] | None = None,
) -> pl.DataFrame:
    sql_info = AzureSqlConnection.from_env()
    engine: sqlalchemy.Engine = sql_info.engine

    return pl.read_database(
        query=query,
        connection=engine,
        #
        iter_batches=iter_batches,
        batch_size=batch_size,
        schema_overrides=schema_overrides,
        infer_schema_length=infer_schema_length,
        execute_options=execute_options,
    )
