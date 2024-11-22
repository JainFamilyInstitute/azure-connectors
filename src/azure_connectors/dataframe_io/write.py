from typing import TYPE_CHECKING, Any, Literal

import sqlalchemy

from azure_connectors import AzureSqlConnection

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl


def write_df(
    df: pl.DataFrame | pl.LazyFrame | pd.DataFrame,
    table_name: str,
    if_table_exists: Literal["append", "replace", "fail"] = "fail",
    **pandas_kwargs: Any,
) -> None:
    """
    Write a DataFrame to a SQL table.
    Parameters:
    df (pl.DataFrame | pl.LazyFrame | pd.DataFrame): The DataFrame to write. Can be a pandas DataFrame, polars DataFrame, or polars LazyFrame.
    table_name (str): The name of the table to write the DataFrame to.
    if_table_exists (Literal["append", "replace", "fail"]): What to do if the table already exists.
        - "append": Append the data to the existing table.
        - "replace": Drop the existing table and create a new one.
        - "fail": Raise an error if the table already exists.
    **pandas_kwargs (Any): Additional keyword arguments to pass to pandas' `to_sql` method.
    Raises:
    TypeError: If the provided DataFrame is not a pandas or polars DataFrame.
    Returns:
    None
    """

    sql_info = AzureSqlConnection.from_env()
    engine: sqlalchemy.Engine = sql_info.engine

    if isinstance(df, pd.DataFrame):
        df.to_sql(
            name=table_name, con=engine, if_exists=if_table_exists, **pandas_kwargs
        )
    elif isinstance(df, pl.LazyFrame | pl.DataFrame):
        if isinstance(df, pl.LazyFrame):
            df = df.collect()

        df.write_database(
            connection=engine,
            table_name=table_name,
            if_table_exists=if_table_exists,
        )
    else:
        raise TypeError(
            "Unsupported DataFrame type. Please provide a pandas or polars DataFrame."
        )
