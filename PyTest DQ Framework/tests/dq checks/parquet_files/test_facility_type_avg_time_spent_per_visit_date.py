"""
Description: Data Quality checks for facility_type_avg_time_spent_per_visit_date parquet file
Requirement: TICKET-1233
Author: Anastasiia Yosypchuk
"""

import pytest

@pytest.fixture(scope='module')
def source_data(db_connection):
    source_query = """
    SELECT
        f.facility_type,
        v.visit_timestamp::date AS visit_date,
        ROUND(AVG(v.duration_minutes), 2) AS avg_time_spent
    FROM
        visits v
    JOIN
        facilities f 
        ON f.id = v.facility_id
    WHERE
        v.visit_timestamp >= '2000-01-01'
        AND f.facility_type IN ('Hospital', 'Clinic', 'Specialty Center', 'Urgent Care')
    GROUP BY
        f.facility_type,
        visit_date;
    """

    source_data = db_connection.get_data_sql(source_query)
    return source_data

@pytest.fixture(scope='module')
def target_data(file_reader):
    target_path = r'/parquet_data/facility_type_avg_time_spent_per_visit_date'
    target_data = file_reader.read(target_path)
    target_data = target_data.drop(columns=["partition_date"])
    return target_data

@pytest.mark.parquet_data
@pytest.mark.smoke
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_dataset_is_not_empty(target_data, data_quality_library):
    data_quality_library.check_dataset_is_not_empty(target_data)


@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_count(source_data, target_data, data_quality_library):
    data_quality_library.check_count(source_data, target_data)


@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_data_completeness(source_data, target_data, data_quality_library):
    data_quality_library.check_data_completeness(source_data, target_data)


@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_duplicates(target_data, data_quality_library):
    data_quality_library.check_duplicates(target_data)


@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_null_values(target_data, data_quality_library):
    data_quality_library.check_null_values(target_data, ['facility_type', 'visit_date', 'avg_time_spent'])


@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_rounding(target_data, data_quality_library):
    data_quality_library.check_rounding(target_data, 'avg_time_spent', 2)

