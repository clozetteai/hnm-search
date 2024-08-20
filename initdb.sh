#!/bin/bash
set -e

until mysql -h 127.0.0.1 -P 4000 -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT 1"; do
  echo "Waiting for TiDB to be ready..."
  sleep 1
done

mysql -h 127.0.0.1 -P 4000 -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
    ALTER USER 'root'@'%' IDENTIFIED BY '$MYSQL_ROOT_PASSWORD';
    FLUSH PRIVILEGES;
EOSQL

echo "TiDB initialized successfully!"


# Manually set password for root user. 
# mysql 127.0.0.1 -P 4000 -u root
# > ALTER USER 'root'@'%' IDENTIFIED BY 'your_new_password_here';
# > FLUSH PRIVILEGES;
# > EXIT