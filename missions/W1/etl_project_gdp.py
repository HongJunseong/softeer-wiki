import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

LOG_FILE = "etl_project_log.txt"
JSON_FILE = "Countries_by_GDP.json"

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def log_progress(message):
    timestamp = datetime.now().strftime("%Y-%B-%d-%H-%M-%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp}, {message}\n")


def extract():
    log_progress("Extract phase Started")

    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    tables = soup.find_all("table", class_="wikitable")
    target_table = None

    for table in tables:
        text = table.get_text(" ", strip=True)
        if "Country/Territory" in text and "IMF" in text and "World Bank" in text:
            target_table = table
            break

    if target_table is None:
        raise Exception("GDP table not found")

    rows = target_table.find_all("tr")
    data = []

    for row in rows[2:]:
        cols = row.find_all(["th", "td"])
        cols = [col.get_text(" ", strip=True) for col in cols]

        if len(cols) >= 4:
            data.append({
                "Country/Territory": cols[0],
                "IMF": cols[1],
                "World Bank": cols[2],
                "United Nations": cols[3]
            })

    df = pd.DataFrame(data)

    log_progress("Extract phase Ended")
    return df


def million_to_billion(x):
    x = str(x)

    # 각주 제거: [1], [2] 등
    x = re.sub(r"\[.*?\]", "", x)

    # 괄호 제거: (2024), (2023) 등
    x = re.sub(r"\(.*?\)", "", x)

    # 쉼표, 대시 제거
    x = x.replace(",", "").replace("—", "").strip()

    try:
        return round(float(x) / 1000, 2)
    except ValueError:
        return None


def transform(df):
    log_progress("Transform phase Started")

    for col in ["IMF", "World Bank", "United Nations"]:
        df[col] = df[col].apply(million_to_billion)

    df.rename(columns={
        "IMF": "IMF (Billion USD)",
        "World Bank": "World Bank (Billion USD)",
        "United Nations": "United Nations (Billion USD)"
    }, inplace=True)

    log_progress("Transform phase Ended")
    return df


def load(df):
    log_progress("Load phase Started")

    df.to_json(
        JSON_FILE,
        orient="records",
        force_ascii=False,
        indent=4
    )

    log_progress("Load phase Ended")


log_progress("ETL Job Started")

df = extract()
df = transform(df)
load(df)

log_progress("ETL Job Ended")

print("ETL finished")
print(df.head())