import polars as pl


def find_n_chunks(df: pl.DataFrame, chunk_size: int) -> int:
    total_chunks = df.shape[0] // chunk_size
    if df.shape[0] % chunk_size != 0:
        total_chunks += 1
    return total_chunks


def get_user_confirmation(question: str) -> None:
    user_input = input(f"{question}\n\tType 'Y' or 'y' to proceed: ").strip()
    if user_input.lower() != "y":
        raise ValueError("Operation aborted by the user.")
