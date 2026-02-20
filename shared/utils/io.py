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
        raise ValueError(f"Unsupported format: {format}")

def load_dataframe(file_path: str, format: str = "csv") -> pd.DataFrame:
    """
    Loads a DataFrame from the specified format.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    if format == "csv":
        return pd.read_csv(file_path)
    elif format == "parquet":
        return pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported format: {format}")
