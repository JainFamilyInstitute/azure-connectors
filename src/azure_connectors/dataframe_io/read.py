from typing import Any, Literal

import polars as pl
import sqlalchemy

from azure_connectors import AzureSqlConnection


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


def get_table_len(table_name: str) -> int:
    """
    Raises:
        sqlalchemy.exc.ProgrammingError: If table does not exist.
    """
    query = f"""--sql
    SELECT COUNT(*) AS TableLength FROM {table_name};
    """
    response: pl.DataFrame = read_df(query)
    return response.item()


if __name__ == "__main__":

    x = get_table_len("votes_raw__dec_25_tablemeta")
    print(x)
    print(type(x))
