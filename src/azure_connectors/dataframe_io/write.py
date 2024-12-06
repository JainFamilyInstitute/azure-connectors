from typing import Literal

import polars as pl
import sqlalchemy

from azure_connectors import AzureSqlConnection


def write_df(
    df: pl.DataFrame | pl.LazyFrame,
    table_name: str,
    if_table_exists: Literal["append", "replace", "fail"],
) -> None:
    sql_info = AzureSqlConnection.from_env()
    engine: sqlalchemy.Engine = sql_info.engine

    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    try:
        df.to_pandas(use_pyarrow_extension_array=True).to_sql(
            con=engine,
            name=table_name,
            if_exists=if_table_exists,
            method="multi",
        )
    except Exception as e:
        df.to_pandas(use_pyarrow_extension_array=False).to_sql(
            con=engine,
            name=table_name,
            if_exists=if_table_exists,
            method="multi",
        )
