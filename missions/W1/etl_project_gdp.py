import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

LOG_FILE = "etl_project_log.txt"      # log file name
JSON_FILE = "Countries_by_GDP.json"   # json file name

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29" # target URL

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Log progress to file
def log_progress(message):
    timestamp = datetime.now().strftime("%Y-%B-%d-%H-%M-%S") # Timestamp format: Year-Month-Day-Hour-Minute-Second

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp}, {message}\n")

# Extract phase
def extract():
    log_progress("Extract phase Started") # Log the start of the extract phase

    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    tables = soup.find_all("table", class_="wikitable") # Find all tables with class "wikitable"
    target_table = None

    for table in tables: # Find the table that contains the GDP data
        text = table.get_text(" ", strip=True)
        if "Country/Territory" in text and "IMF" in text and "World Bank" in text:
            target_table = table
            break

    if target_table is None: # If the target table is not found, raise an exception
        raise Exception("GDP table not found")

    rows = target_table.find_all("tr")
    data = []

    for row in rows[2:]: # Skip the first two rows (header rows)
        cols = row.find_all(["th", "td"])
        cols = [col.get_text(" ", strip=True) for col in cols]

        if len(cols) >= 4:
            data.append({
                "Country/Territory": cols[0],
                "IMF": cols[1],
                "World Bank": cols[2],
                "United Nations": cols[3]
            })

    df = pd.DataFrame(data) # Create a DataFrame from the extracted data

    log_progress("Extract phase Ended") # Log the end of the extract phase
    return df


# Clean and transform the GDP values from million to billion
def million_to_billion(x):
    x = str(x)

    # remove brackets: [1], [2] etc.
    x = re.sub(r"\[.*?\]", "", x)

    # remove parentheses: (2024), (2023) etc.
    x = re.sub(r"\(.*?\)", "", x)

    # remove commas, dashes
    x = x.replace(",", "").replace("—", "").strip()

    try: # Convert to float and divide by 1000 to convert million to billion
        return round(float(x) / 1000, 2)
    except ValueError:
        return None

# Clean country names by removing brackets and extra spaces    
def clean_country_name(x):

    x = str(x)
    x = re.sub(r"\[.*?\]", "", x)   # [n 1], [1] 제거
    x = re.sub(r"\s+", " ", x)      # 여러 공백 정리

    return x.strip()

# Transform phase
def transform(df):
    log_progress("Transform phase Started") # Log the start of the transform phase

    df["Country/Territory"] = df["Country/Territory"].apply(clean_country_name)

    for col in ["IMF", "World Bank", "United Nations"]: # Convert the GDP values from million to billion
        df[col] = df[col].apply(million_to_billion)

    df.rename(columns={
        "IMF": "IMF (Billion USD)",
        "World Bank": "World Bank (Billion USD)",
        "United Nations": "United Nations (Billion USD)"
    }, inplace=True)

    log_progress("Transform phase Ended") # Log the end of the transform phase
    return df


def load(df):
    log_progress("Load phase Started") # Log the start of the load phase

    df.to_json(
        JSON_FILE,
        orient="records",
        force_ascii=False,
        indent=4
    )

    log_progress("Load phase Ended") # Log the end of the load phase


log_progress("ETL Job Started") # Log the start of the ETL job

df = extract()     # Extract the data from the Wikipedia page
df = transform(df) # Transform the extracted data
load(df)           # Load the transformed data into a JSON file

log_progress("ETL Job Ended") # Log the end of the ETL job

print("ETL finished")
print(df.head())