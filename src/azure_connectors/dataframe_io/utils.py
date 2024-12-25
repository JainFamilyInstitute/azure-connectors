import polars as pl


def find_n_chunks(df: pl.DataFrame, chunk_size: int) -> int:
    total_chunks = df.shape[0] // chunk_size
    if df.shape[0] % chunk_size != 0:
        total_chunks += 1
    return total_chunks
