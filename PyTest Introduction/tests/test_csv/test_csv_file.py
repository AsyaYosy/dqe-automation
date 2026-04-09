import pytest
import re

def test_file_not_empty(read_csv_file):
    assert read_csv_file.empty, "CSV file is empty"


@pytest.mark.validate_csv
@pytest.mark.xfail
def test_duplicates(read_csv_file):
    duplicates = read_csv_file.duplicated()
    assert not duplicates.any(), "CSV file contains duplicate rows"


@pytest.mark.validate_csv
def test_validate_schema(actual_schema, expected_schema):
    assert actual_schema == expected_schema, "Schema does not match expected schema"
    

@pytest.mark.validate_csv
@pytest.mark.skip
def test_age_column_valid(read_csv_file):
    valid_age = [0, 100]
    age = read_csv_file['age']
    age_not_null = age[age.notna()]
    assert age_not_null.between(valid_age[0], valid_age[1]).all(), "Age column contains invalid values"


@pytest.mark.validate_csv
def test_email_column_valid(read_csv_file):
    email = read_csv_file["email"]
    email_not_null = email[email.notna()]
    email_pattern = r"^[a-z0-9_.]+@[a-z0-9_.]+\.[a-z]{2,}$"
    assert email_not_null.str.match(email_pattern).all(), "Email column contains invalid email addresses"


def test_active_players(read_csv_file):
    df = read_csv_file[["id", "is_active"]]
    players_1 =  df[df["id"] == 1]["is_active"]
    players_2 =  df[df["id"] == 2]["is_active"]
    
    assert (players_1 == False).all(), "Player with id 1 should be inactive"
    assert (players_2 == True).all(), "Player with id 2 should be active"


@pytest.mark.parametrize("id, expected_status", [(1, False), (2, True)])
def test_active_player(read_csv_file, id, expected_status):
    df = read_csv_file[["id", "is_active"]]
    actual_status = df[df["id"] == id]["is_active"]

    assert (actual_status == expected_status).all(), f"Player with id {id} should have is_active status {expected_status}"
