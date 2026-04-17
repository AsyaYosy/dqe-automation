import pandas as pd
from pathlib import Path

class FileReader:
    """
    A class for reading data from files. This class provides a common interface
    for different file formats (e.g., Parquet, CSV, JSON) and can be extended to
    implement specific readers for each format.
    """

    def read(self, file_path):
        path = Path(file_path)
        suffix = path.suffix.lower()
        if suffix == '.parquet' or suffix == '':
            return self._read_parquet(file_path)
        elif suffix == '.csv':
            return self._read_csv(file_path)
        elif suffix == '.json':
            return self._read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
