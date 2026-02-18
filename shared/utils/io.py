import os
import pandas as pd

def save_dataframe(df: pd.DataFrame, file_path: str, format: str = "csv"):
    """
    Saves a DataFrame to the specified format (csv or parquet).
    Creates directories if they don't exist.
    """
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    if format == "csv":
        df.to_csv(file_path, index=False)
    elif format == "parquet":
        df.to_parquet(file_path, index=False)
    else:
