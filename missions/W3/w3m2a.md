# Hadoop Multi-Node Cluster on Docker

## 1. 멀티 노드 클러스터 구성

이번 미션에서는 Docker를 활용하여 Hadoop 멀티 노드 클러스터를 구축하였다.

- NameNode와 여러 DataNode를 구성했다.
- Docker Compose를 이용해 여러 컨테이너를 함께 실행했다.

이를 통해 하나의 Hadoop 클러스터를 여러 노드로 구성하는 방법을 배웠다.

## 2. HDFS 분산 저장

HDFS가 여러 DataNode를 활용하는 방식을 확인하였다.

- 데이터를 HDFS에 저장하고 조회했다.
- 복제(Replication)를 통해 데이터가 여러 노드에 저장되는 구조를 이해했다.

이를 통해 HDFS가 데이터를 분산 저장하여 안정성을 높인다는 점을 배웠다.

## 3. 클러스터 관리

클러스터의 동작 상태를 확인하는 방법을 익혔다.

- NameNode와 DataNode의 연결 상태를 확인했다.
- 웹 UI를 통해 클러스터 정보를 확인했다.

이번 미션을 통해 Docker 환경에서 Hadoop 멀티 노드 클러스터를 구성하고 관리하는 기본 방법을 익힐 수 있었다.