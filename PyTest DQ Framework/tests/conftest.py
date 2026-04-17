import pytest
from src.connectors.postgres.postgres_connector import PostgresConnectorContextManager
from src.connectors.mysql.mysql_connector import MySqlConnectorContextManager
from src.connectors.oracle.oracle_connector import OracleConnectorContextManager

from src.data_quality.data_quality_validation_library import DataQualityLibrary
from src.connectors.file_system.file_reader import FileReader

def pytest_addoption(parser):
    parser.addoption("--db_host", action="store", default="localhost", help="Database host")
    parser.addoption("--db_name", action="store", default="my_database", help="Database name")
    parser.addoption("--db_port", action="store", default="5432", help="Database port")
    parser.addoption("--db_user", action="store", default="myuser", help="Database user")
    parser.addoption("--db_password", action="store", default="mypassword", help="Database password")

def pytest_configure(config):
    """
    Validates that all required command-line options are provided.
    """
    required_options = [
        "db_user", "db_password"
    ]
    for option in required_options:
        if not config.getoption(option):
            pytest.fail(f"Missing required option: --{option}")

@pytest.fixture(scope='session')
def db_connection(request):
    db_type = request.config.getoption("--db_type")
    db_host = request.config.getoption("--db_host")
    db_name = request.config.getoption("--db_name")
    db_port = request.config.getoption("--db_port")
    db_user = request.config.getoption("--db_user")
    db_password = request.config.getoption("--db_password")

    connector_class = None

    if db_type == "postgres":
        connector_class = PostgresConnectorContextManager
    elif db_type == "mysql":
        connector_class = MySqlConnectorContextManager
    elif db_type == "oracle":
        connector_class = OracleConnectorContextManager

    try:
        with connector_class(db_user=db_user, db_password=db_password, db_host=db_host,
                            db_name=db_name, db_port=db_port) as db_connector:
            yield db_connector
    except Exception as e:
        pytest.fail(f"Failed to initialize {connector_class.__name__}: {e}")


@pytest.fixture(scope='session')
def file_reader(request):
    try:
        reader = FileReader()
        yield reader
    except Exception as e:
        pytest.fail(f"Failed to initialize FileReader: {e}")
    finally:
        del reader


@pytest.fixture(scope='session')
def data_quality_library():
    try:
        data_quality_library = DataQualityLibrary()
        yield data_quality_library
    except Exception as e:
        pytest.fail(f"Failed to initialize DataQualityLibrary: {e}")
    finally:
        del data_quality_library
