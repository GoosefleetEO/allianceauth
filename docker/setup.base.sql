CREATE USER 'aauth'@'%' IDENTIFIED BY 'authpass';
CREATE USER 'grafana'@'%' IDENTIFIED BY 'grafanapass';
CREATE DATABASE alliance_auth CHARACTER SET utf8mb4;
GRANT ALL PRIVILEGES ON alliance_auth.* TO 'aauth'@'%';
GRANT
SELECT,
    SHOW VIEW ON alliance_auth.* TO 'grafana'@'%';
