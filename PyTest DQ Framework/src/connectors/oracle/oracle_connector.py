import pandas as pd
import oracledb

class OracleConnectorContextManager:
    def __init__(self, db_host: str, db_name: str, db_user: str, db_password: str, db_port: str):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port
        self.connection = None

    def __enter__(self):
        dsn = f"{self.db_host}:{self.db_port}/{self.db_name}"
        self.connection = oracledb.connect(
            user=self.db_user,
            password=self.db_password,
            dsn=dsn
        )
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.connection:
            self.connection.close()

    def execute_query(self, query: str):
        return pd.read_sql(query, self.connection)
 
        


