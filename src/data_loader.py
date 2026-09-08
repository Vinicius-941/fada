import pandas as pd

from src.config import DATABASE_PATH


def load_transactions(path=DATABASE_PATH):
    try:
        return pd.read_csv(path, sep=";", encoding="utf-8-sig")
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Database file was not found: {path}") from error
