from typing import Literal

import polars as pl
import sqlalchemy

from azure_connectors import AzureSqlConnection
from azure_connectors.dataframe_io.utils import get_user_confirmation

from . import dataframe_io_config
from .insertion_methods import pl_to_sql_row_by_row, pl_to_sql_via_pandas
from .read import get_table_len


def write_df(
    df: pl.DataFrame | pl.LazyFrame,
    table_name: str,
    if_table_exists: Literal["append", "replace", "fail"],
) -> None:
    sql_info = AzureSqlConnection.from_env()
    engine: sqlalchemy.Engine = sql_info.engine

    if isinstance(df, pl.LazyFrame):
        df = df.collect()

    pl_to_sql_via_pandas(
        df,
        table_name=table_name,
        if_table_exists=if_table_exists,
        engine=engine,
    )


def write_df_from_sqltable(
    df: pl.DataFrame | pl.LazyFrame,
    if_table_exists: Literal["append", "replace", "fail", "resume"],
    table: sqlalchemy.Table,
    chunk_size: int = dataframe_io_config.DEFAULT_WRITE_CHUNKSIZE,
    insertion_method: Literal[
        "pl_to_sql_via_pandas", "pl_to_sql_row_by_row"
    ] = "pl_to_sql_row_by_row",
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
    if not all(k in df.columns for k in primary_keys):
        raise ValueError(
            f"At least one primary key is missing from the columns.\n{primary_keys=}\n{df.columns=}"
        )
    if len(primary_keys) == 0:
        raise ValueError("Must provide a primary key:\n", table)

    any_pk_rows_duplicated: bool = df.select(
        pl.any_horizontal(pl.col(primary_keys).is_duplicated().any())
    ).item()
    if any_pk_rows_duplicated:
        offending_observations = df.filter(pl.col(primary_keys).is_duplicated()).sort(
            primary_keys
        )
        raise ValueError(
            f"df must be unique on {primary_keys=}.",
            "The following observations have >1 unique value corresponding to the same unique primary_key (i.e., these are the observations causing this error):",
            offending_observations,
        )
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
                # print("Dropping table")
                get_user_confirmation(
                    f"This operation will overwrite the existing `{table.name}` table."
                )
                table.drop(engine, checkfirst=True)
                table_exists = False
            pass
        case "append":
            pass
        case "resume":
            if table_exists:
                current_table_len: int = get_table_len(table.name)
                df = df.slice(offset=current_table_len)
                get_user_confirmation(
                    f"Resuming upload of `{table.name}` from row {current_table_len:_}. {df.shape[0]:_} rows remaining, or {df.shape[0]//chunk_size:_} chunks of size {chunk_size:_}."
                )
        case _:
            raise ValueError('if_table_exists not in ["append", "replace", "fail"].')

    # create table
    if not table_exists:
        print("Creating table")
        table.create(engine, checkfirst=True)

    # cast `resume`
    if_table_exists_no_resume: Literal["append", "replace", "fail"] = (
        "append" if if_table_exists == "resume" else if_table_exists
    )

    # insert data
    match insertion_method:
        case "pl_to_sql_via_pandas":
            pl_to_sql_via_pandas(
                df,
                table_name=table.name,
                if_table_exists=if_table_exists_no_resume,
                engine=engine,
                chunk_size=chunk_size,
            )
        case "pl_to_sql_row_by_row":
            pl_to_sql_row_by_row(
                df,
                table=table,
                engine=engine,
                chunk_size=chunk_size,
            )
        case _:
            raise ValueError(
                f"{insertion_method=} not in ['pl_to_sql_via_pandas', 'pl_to_sql_row_by_row']"
            )


if __name__ == "__main__":
    df = pl.DataFrame({"a": range(10_000)})
    metadata = sqlalchemy.MetaData()
    table = sqlalchemy.Table(
        "write_df_from_sqltable_test",
        metadata,
        sqlalchemy.Column("a", sqlalchemy.Integer, nullable=False, primary_key=True),
    )
    write_df_from_sqltable(
        df,
        if_table_exists="replace",
        table=table,
        chunk_size=10_000,
        insertion_method="pl_to_sql_row_by_row",
    )
