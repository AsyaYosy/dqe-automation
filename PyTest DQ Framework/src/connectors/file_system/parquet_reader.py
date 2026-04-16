import pandas as pd

class ParquetReader:
    def read_parquet(self, file_path: str):
        return pd.read_parquet(file_path)