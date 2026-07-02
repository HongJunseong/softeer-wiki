import pandas as pd
import sqlite3
import country_converter as coco

# JSON 읽기
df = pd.read_json("Countries_by_GDP.json")

# Region 컬럼 추가
cc = coco.CountryConverter()
df["Region"] = cc.convert(
    names=df["Country/Territory"],
    to="continent"
)

# country_converter에서 변환되지 않은 국가를 수동으로 지정
manual_region = {
    "Channel Islands": "Europe",
    "Zanzibar": "Africa",
}
for country, region in manual_region.items():
    df.loc[df["Country/Territory"] == country, "Region"] = region

# SQLite 연결
conn = sqlite3.connect("World_Economies.db")
cursor = conn.cursor()

# 테이블 저장
df.to_sql(
    "Countries_by_GDP",
    conn,
    if_exists="replace",
    index=False
)

print("\n===== GDP 100 Billion USD 이상 국가 =====")
cursor.execute('''
SELECT * FROM Countries_by_GDP WHERE "IMF (Billion USD)" >= 100;
''')

rows = cursor.fetchall()
for row in rows:
    print(row)


print("\n===== Region별 Top 5 국가 GDP 평균 =====")
# 1. DB에 있는 Region 목록 가져오기

cursor.execute("""
SELECT DISTINCT Region
FROM Countries_by_GDP
WHERE Region IS NOT NULL;
""")
regions = cursor.fetchall()

# 2. 각 Region별 GDP Top 5 평균 구하기
for region in regions:
    region_name = region[0]
    cursor.execute("""
    SELECT ROUND(AVG("IMF (Billion USD)"), 2)
    FROM (
        SELECT "IMF (Billion USD)"
        FROM Countries_by_GDP
        WHERE Region = ?
          AND "IMF (Billion USD)" IS NOT NULL
        ORDER BY "IMF (Billion USD)" DESC
        LIMIT 5
    );
    """, (region_name,))
    avg_gdp = cursor.fetchone()[0]
    print(f"{region_name} : {avg_gdp}")

conn.close()