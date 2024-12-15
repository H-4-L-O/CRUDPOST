# DockerFile(MySQL)

# MySQL 8.0
FROM mysql:8.0

# 환경 변수
ENV MYSQL_ROOT_PASSWORD=1234
ENV MYSQL_DATABASE=CRUDPOST
ENV MYSQL_USER=halo
ENV MYSQL_PASSWORD=1234

# 초기화 SQL 스크립트 복사
COPY init.sql /docker-entrypoint-initdb.d/

# MySQL 컨테이너 포트
EXPOSE 3306
