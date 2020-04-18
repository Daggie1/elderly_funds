psql -U postgres -c "CREATE USER postgres PASSWORD 'toor'"
psql -U postgres -c "CREATE DATABASE edms7 OWNER postgres"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE edms7 TO postgres"