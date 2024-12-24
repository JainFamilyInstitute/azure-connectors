from typing import Literal

import polars as pl
import sqlalchemy

from azure_connectors import AzureSqlConnection

from .utils import pl_to_sql


def write_df(
    df: pl.DataFrame | pl.LazyFrame,
    table_name: str,
    if_table_exists: Literal["append", "replace", "fail"],
) -> None:
    sql_info = AzureSqlConnection.from_env()
    engine: sqlalchemy.Engine = sql_info.engine

    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    pl_to_sql(
        df,
        table_name=table_name,
        if_table_exists=if_table_exists,
        engine=engine,
    )


def write_df_from_sqltable(
    df: pl.DataFrame | pl.LazyFrame,
    if_table_exists: Literal["append", "replace", "fail"],
    table: sqlalchemy.Table,
) -> None:
    """
    `table` param example:

    ```python
    table = Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50, collation="Latin1_General_CI_AI"), nullable=False),
        Column("age", Integer, nullable=False),
        Column("account_id", Integer, ForeignKey("accounts.account_id"),nullable=False)
    )
    ```
    """
    sql_info = AzureSqlConnection.from_env()
    engine: sqlalchemy.Engine = sql_info.engine

    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    # PRIMARY KEY CHECKS
    primary_keys: list[str] = [col.name for col in table.primary_key.columns]
    if len(primary_keys) == 0:
        raise ValueError("Must provide a primary key:\n", table)

    any_pk_rows_duplicated: bool = df.select(
        pl.any_horizontal(pl.col(["name", "age"]).is_duplicated().any())
    ).item()
    if any_pk_rows_duplicated:
        raise ValueError(f"df must be unique on {primary_keys=}")
    # / PRIMARY KEY CHECKS

    inspector = sqlalchemy.inspect(engine)
    table_exists: bool = inspector.has_table(
        table.name,
        # schema=table.schema,
    )

    # ensure table exists, and has been wiped if specified
    match if_table_exists:
        case "fail":
            if table_exists:
                raise ValueError("Table already exists:", table)
            pass
        case "replace":
            if table_exists:
                print("Dropping table")
                table.drop(engine, checkfirst=True)
            pass
        case "append":
            pass
        case _:
            raise ValueError('if_table_exists not in ["append", "replace", "fail"].')

    # create table
    if not table_exists:
        print("Creating table")
        table.create(engine, checkfirst=True)

    # insert data
    pl_to_sql(
        df,
        table_name=table.name,
        if_table_exists=if_table_exists,
        engine=engine,
    )
