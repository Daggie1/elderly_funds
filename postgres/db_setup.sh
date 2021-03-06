set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER edms;
    CREATE DATABASE work;
    GRANT ALL PRIVILEGES ON DATABASE work TO edms;
EOSQL
