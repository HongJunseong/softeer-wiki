# Week 6

6주차에는 Apache Airflow를 활용하여 **서울 공공자전거 데이터를 수집·변환·적재하는 ETL 파이프라인**을 구축하며 데이터 파이프라인의 전체적인 처리 흐름을 학습했다.

또한 동일한 작업을 여러 번 실행하거나 실패 후 재실행하더라도 중복 없이 동일한 결과를 생성할 수 있도록 **멱등성(Idempotency)**을 고려하여 파이프라인을 설계하였다. 이를 통해 Airflow의 DAG와 Task를 활용한 워크플로우 관리와 안정적인 데이터 파이프라인 구축 방법을 익혔다.

## Missions

| Mission | Topic |
|---|---|
| [W6M1](./w6m1.md) | Building an Idempotent ETL Pipeline using Airflow |