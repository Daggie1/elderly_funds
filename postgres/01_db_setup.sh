psql -U postgres -c "CREATE USER allan PASSWORD 'password'"
psql -U postgres -c "CREATE DATABASE work OWNER allan"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE work TO allan"