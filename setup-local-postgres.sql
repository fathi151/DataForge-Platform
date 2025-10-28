-- Create databases for the data platform
-- Run this script on your local PostgreSQL installation

-- Create airflow database
CREATE DATABASE airflow;

-- Create datawarehouse database
CREATE DATABASE datawarehouse;

-- Create user if not exists
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'datauser') THEN
      CREATE ROLE datauser WITH LOGIN PASSWORD 'datapass123';
   END IF;
END
$do$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE airflow TO datauser;
GRANT ALL PRIVILEGES ON DATABASE datawarehouse TO datauser;

-- Connect to airflow database and grant schema privileges
\c airflow
GRANT ALL PRIVILEGES ON SCHEMA public TO datauser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO datauser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO datauser;

-- Connect to datawarehouse database and grant schema privileges
\c datawarehouse
GRANT ALL PRIVILEGES ON SCHEMA public TO datauser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO datauser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO datauser;
