import pytest
import pandas as pd

# Fixture to provide the path to the CSV file
@pytest.fixture(scope="session")
def path_to_file(pytestconfig):
    return pytestconfig.rootpath.parent / "src" / "data" / "data.csv"


# Fixture to read the CSV file
@pytest.fixture(scope="session")
def read_csv_file(path_to_file):
    return pd.read_csv(path_to_file)


# Fixture to validate the schema of the file
@pytest.fixture(scope="session")
def expected_schema():
    return ["id", "name", "age", "email", "is_active"]

@pytest.fixture(scope="session")
def actual_schema(read_csv_file):
    return list(read_csv_file.columns)


# Pytest hook to mark unmarked tests with a custom mark
def pytest_collection_modifyitems(config, items):
    for item in items:
        if not list(item.iter_markers()):
            item.add_marker(pytest.mark.unmarked)

