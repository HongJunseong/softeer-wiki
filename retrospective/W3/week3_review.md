# Week3 회고

3주차에는 Docker를 기반으로 Hadoop Single-Node와 Multi-Node Cluster를 직접 구축하고, HDFS와 YARN의 동작 원리를 실습하며 분산 처리 환경을 경험했습니다. 또한 MapReduce를 활용해 Word Count, Twitter 감성 분석, 영화 평점 평균 계산, Amazon 리뷰 분석 등 다양한 데이터를 처리하며 Mapper와 Reducer가 데이터를 분산 처리하는 과정을 이해할 수 있었습니다. 단순히 예제를 실행하는 것에 그치지 않고, Hadoop 설정 파일과 클러스터 구조가 실제로 어떤 역할을 하는지 확인하며 분산 시스템의 기본 구조를 익힐 수 있었습니다.

다만 Hadoop 환경을 직접 구성하는 과정에서 설정 파일과 Docker 환경을 충분히 이해하지 못해 오류를 해결하는 데 많은 시간이 소요되었습니다. 또한 MapReduce 문제마다 Key-Value 구조와 Mapper, Reducer의 로직을 설계하는 방식이 달라 처음에는 데이터를 어떤 형태로 처리해야 하는지 어려움을 느꼈습니다. 다음 주차에는 실습한 내용을 다시 정리하며 Hadoop의 핵심 설정과 데이터 처리 흐름을 복습하고, 다양한 데이터를 직접 처리해 보면서 분산 처리와 MapReduce에 대한 이해를 더욱 깊게 만들어 나가겠습니다.