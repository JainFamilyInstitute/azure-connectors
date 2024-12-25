from typing import Literal

import polars as pl
import sqlalchemy
from tqdm.auto import tqdm

from . import dataframe_io_config


def pl_to_sql_via_pandas(
    df: pl.DataFrame,
    table_name: str,
    if_table_exists: Literal["append", "replace", "fail"],
    engine: sqlalchemy.Engine,
    chunk_size: int = 100,
) -> None:
    try:
        df.to_pandas(use_pyarrow_extension_array=True).to_sql(
            con=engine,
            name=table_name,
            if_exists=if_table_exists,
            method="multi",
            index=False,
            chunksize=dataframe_io_config.DEFAULT_WRITE_CHUNKSIZE,
        )
    except Exception as e:
        print("Failed writing to df when using pyarrow to convert pl --> pd:", e)
        df.to_pandas(use_pyarrow_extension_array=False).to_sql(
            con=engine,
            name=table_name,
            if_exists=if_table_exists,
            method="multi",
            index=False,
            chunksize=dataframe_io_config.DEFAULT_WRITE_CHUNKSIZE,
        )


def pl_to_sql_row_by_row(
    df: pl.DataFrame,
    table: sqlalchemy.Table,
    engine: sqlalchemy.Engine,
    chunk_size: int = 100,
) -> None:
    insert_statement = sqlalchemy.insert(table)
    with engine.begin() as conn:
        for i, chunk in tqdm(
            enumerate(df.iter_slices(dataframe_io_config.DEFAULT_WRITE_CHUNKSIZE))
        ):
            try:
                conn.execute(insert_statement, chunk.rows(named=True))
            except Exception as e:
                print(
                    f"`pl_to_sql_row_by_row` failed while executing {insert_statement} on chunk #{i}.\n{chunk=}"
                )
                raise e
