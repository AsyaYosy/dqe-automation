*** Settings ***
Library    SeleniumLibrary
Library    helper.py
*** Variables ***
${REPORT_FILE}       C:/Users/AnastasiiaYosypchuk/DQA/HW1_CICD_Introduction/generated_report/report.html
${PARQUET_FOLDER}    C:/Users/AnastasiiaYosypchuk/DQA/HW1_CICD_Introduction/parquet_data/facility_type_avg_time_spent_per_visit_date
${FILTER_LAST_DAYS}   6
*** Test Cases ***
Compare HTML Report With Parquet Data
   Open Browser    file:///${REPORT_FILE}    Chrome
   Wait Until Element Is Visible    class:table    timeout=10s
   ${table}=    Get WebElement    class:table
   ${html_df}=    Read Plotly Table    ${table}
   Log  ${html_df}
   ${parquet_df}=    Read Parquet Data    ${PARQUET_FOLDER}    ${FILTER_LAST_DAYS}
   Log  ${parquet_df}
   ${is_equal}    ${message}=    Compare Dataframes    ${html_df}    ${parquet_df}
   IF    not ${is_equal}
       Fail    ${message}
   END
   Close Browser