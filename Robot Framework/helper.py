import pandas as pd
from selenium.webdriver.common.by import By


def read_plotly_table(table_element):
    columns = table_element.find_elements(By.CLASS_NAME, "y-column")
    data = {}
    values = []

    for column in columns:
        values = []
        header = column.find_element(By.ID, "header").text.strip()
        cells = column.find_elements(By.CLASS_NAME, "cell-text")
        for cell in cells:
            text = cell.text.strip()
            if text and text != header:
                values.append(text)
        data[header] = values

    df = pd.DataFrame(data)
    df = df.rename(columns={
        "Facility Type": "facility_type",
        "Visit Date": "visit_date",
        "Average Time Spent": "avg_time_spent"
    })
    df["avg_time_spent"] = pd.to_numeric(df["avg_time_spent"])

    return df


def read_parquet_data(parquet_file, filter_last_days=None):
    df = pd.read_parquet(parquet_file).drop(columns=['partition_date'])
    df['visit_date'] = pd.to_datetime(df['visit_date'])
    
    if not filter_last_days:
        return df.reset_index(drop=True)

    last_loaded_date = df['visit_date'].max()
    last_week_data = df[df['visit_date'] >= (last_loaded_date - pd.Timedelta(days=int(filter_last_days)))]
    df_last_week_data = last_week_data.sort_values(by=['visit_date', 'facility_type'], ascending=False)

    return df_last_week_data.reset_index(drop=True)


def compare_dataframes(html_df, parquet_df):
    html_df = html_df.astype(str).reset_index(drop=True)
    parquet_df = parquet_df.astype(str).reset_index(drop=True)
    if html_df.equals(parquet_df):
        return True, "The data in the HTML table matches the data in the Parquet file."
    else:
        return False, "The data in the HTML table does NOT match the data in the Parquet file."
