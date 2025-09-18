-- Create database
CREATE DATABASE boneca;

-- Switch to boneca database
\c boneca;

-- Create schema
CREATE SCHEMA boneca;

-- Create development user
CREATE USER boneca WITH PASSWORD 'boneca';

-- Grant privileges to boneca user
GRANT CONNECT ON DATABASE boneca TO boneca;
GRANT USAGE ON SCHEMA boneca TO boneca;
GRANT CREATE ON SCHEMA boneca TO boneca;

-- Grant all privileges on all tables in schema boneca to boneca user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA boneca TO boneca;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA boneca TO boneca;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA boneca TO boneca;

-- Grant default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA boneca GRANT ALL ON TABLES TO boneca;
ALTER DEFAULT PRIVILEGES IN SCHEMA boneca GRANT ALL ON SEQUENCES TO boneca;
ALTER DEFAULT PRIVILEGES IN SCHEMA boneca GRANT ALL ON FUNCTIONS TO boneca;

-- Set default schema for boneca user
ALTER USER boneca SET search_path TO boneca, public;