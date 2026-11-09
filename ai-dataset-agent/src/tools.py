
import pandas as pd

DATASET_PATH = "data/sales.csv"


def inspect_schema() -> dict:
    """
    Inspect the dataset structure without using an LLM.
    """
    df = pd.read_csv(DATASET_PATH)

    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": [
            {
                "name": col,
                "dtype": str(df[col].dtype)
            }
            for col in df.columns
        ]
    }


