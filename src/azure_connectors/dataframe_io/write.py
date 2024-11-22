from typing import Literal
from azure_connectors import AzureSqlConnection
import sqlalchemy
import polars as pl


def write_df(
    df: pl.DataFrame | pl.LazyFrame,
    table_name: str,
    if_table_exists: Literal["append", "replace", "fail"],
) -> None:
    sql_info = AzureSqlConnection.from_env()
    engine: sqlalchemy.Engine = sql_info.engine

    if isinstance(df, pl.LazyFrame):
        df = df.collect()
    
    df.write_database(
        connection=engine,
        table_name=table_name,
        if_table_exists=if_table_exists,
    )