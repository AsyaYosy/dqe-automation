import time
import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class SeleniumWebDriverContextManager:
    def __init__(self):
        self.driver = None

    def __enter__(self) -> WebDriver:
        option = webdriver.ChromeOptions()
        option.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=option)
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver:
            self.driver.quit()


def get_report_file_url():
    file_path = os.path.abspath("report.html")
    return f"file:///{file_path.replace(os.sep, '/')}"

#2.Table Intaraction
def extract_table_to_csv(driver):
    output_file="table.csv"

    try:
        wait = WebDriverWait(driver, 10)
        table = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@class="table"]'))
        )
        columns = table.find_elements(By.CLASS_NAME, "y-column")
        if not columns:
            raise NoSuchElementException("Columns with class 'y-column' were not found")


        table_data = {}
        for column in columns:
            #ID locator
            header = column.find_element(By.ID, "header").text.strip()
            cells = column.find_elements(By.CLASS_NAME, "cell-text")
            values = []
            for cell in cells:
                text = cell.text.strip()
                # skip empty text and duplicated header text
                if text and text != header:
                    values.append(text)
            table_data[header] = values

        df = pd.DataFrame(table_data)
        df.to_csv(output_file, index=False)
        print(f"Table data saved to {output_file}")

    except TimeoutException:
        print("Table was not loaded in time")
    except Exception as e:
        print(f"Unexpected error: {e}")


#3.Doughnut Chart Intaraction
def save_doughnut_data_to_csv(driver, output_file):
    doughnut = driver.find_element(By.CLASS_NAME, "pielayer")
    labels = doughnut.find_elements(By.CSS_SELECTOR, "text.slicetext[data-notex='1']")
    rows = []
    for label in labels:
        tspans = label.find_elements(By.TAG_NAME, "tspan")
        facility_type = tspans[0].text.strip()
        min_average_time_spent = tspans[1].text.strip()

        rows.append([facility_type, min_average_time_spent])

    df = pd.DataFrame(rows, columns=["Facility Type", "Min Average Time Spent"])
    df.to_csv(output_file, index=False)


def interact_with_doughnut_chart(driver, report_url):
    try:
        wait = WebDriverWait(driver, 10)

        #initial state
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "pielayer"))
        )
        time.sleep(2)
        driver.save_screenshot("screenshot0.png")
        save_doughnut_data_to_csv(driver, "doughnut0.csv")


        legend_box = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "scrollbox"))
        )
        legend_items = legend_box.find_elements(By.CLASS_NAME, "traces")
        legend_count = len(legend_items)

        for i in range(legend_count):
            #reload page to reset filters
            driver.get(report_url)
            time.sleep(2)
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "pielayer"))
            )
            legend_box = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "scrollbox"))
            )
            legend_items = legend_box.find_elements(By.CLASS_NAME, "traces")
            current_item = legend_items[i]
            current_item.click()
            time.sleep(1)
            driver.save_screenshot(f"screenshot{i + 1}.png")
            save_doughnut_data_to_csv(driver, f"doughnut{i + 1}.csv")

        #all filters unselected
        try:
            driver.get(report_url)
            time.sleep(2)
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "scrollbox"))
            )
            legend_box = driver.find_element(By.CLASS_NAME, "scrollbox")
            legend_items = legend_box.find_elements(By.CLASS_NAME, "traces")
            for item in legend_items:
                driver.execute_script("arguments[0].scrollIntoView(true);", item)
                time.sleep(1)
                item.click()
                time.sleep(1)
            edge_case_index = legend_count + 1
            driver.save_screenshot(f"screenshot{edge_case_index}.png")
            save_doughnut_data_to_csv(driver, f"doughnut{edge_case_index}.csv")
        except Exception as e:
            print(f"Could not save edge case with all filters unselected: {e}")

    except TimeoutException:
        print("Doughnut chart was not loaded in time")
    except NoSuchElementException as e:
        print(f"Chart element not found: {e}")
    except Exception as e:
        print(f"Unexpected error in doughnut chart interaction: {e}")

if __name__ == "__main__":
    with SeleniumWebDriverContextManager() as driver:
        report_url = get_report_file_url()

        driver.get(report_url)
        time.sleep(2)
        extract_table_to_csv(driver)

        driver.get(report_url)
        time.sleep(2)
        interact_with_doughnut_chart(driver, report_url)