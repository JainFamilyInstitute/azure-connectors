from typing import Literal

import polars as pl
import sqlalchemy


def pl_to_sql(
    df: pl.DataFrame,
    table_name: str,
    if_table_exists: Literal["append", "replace", "fail"],
    engine: sqlalchemy.Engine,
) -> None:
    try:
        df.to_pandas(use_pyarrow_extension_array=True).to_sql(
            con=engine,
            name=table_name,
            if_exists=if_table_exists,
            method="multi",
            index=False,
        )
    except Exception as e:
        print("Failed writing to df when using pyarrow to convert pl --> pd:", e)
        df.to_pandas(use_pyarrow_extension_array=False).to_sql(
            con=engine,
            name=table_name,
            if_exists=if_table_exists,
            method="multi",
        )
