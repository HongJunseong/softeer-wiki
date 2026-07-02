import pandas as pd
import sqlite3

# JSON 읽기
df = pd.read_json("Countries_by_GDP.json")

# SQLite 연결
conn = sqlite3.connect("World_Economies.db")
cursur = conn.cursor()

# 테이블 저장

df.to_sql(
    "Countries_by_GDP",
    conn,
    if_exists="replace",
    index=False
)

cursur.execute('''
SELECT * FROM Countries_by_GDP WHERE "IMF (Billion USD)" >= 100;
''')

rows = cursur.fetchall()
for row in rows:
    print(row)

conn.close()
print("Save to SQLite completed")