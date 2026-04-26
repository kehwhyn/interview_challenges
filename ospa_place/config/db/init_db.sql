-- Create schemas for data warehouse
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- Grant privileges to public
GRANT USAGE ON SCHEMA bronze TO public;
GRANT USAGE ON SCHEMA silver TO public;
GRANT USAGE ON SCHEMA gold TO public;

GRANT CREATE ON SCHEMA bronze TO public;
GRANT CREATE ON SCHEMA silver TO public;
GRANT CREATE ON SCHEMA gold TO public;

ALTER DATABASE dop SET search_path TO public, bronze, silver, gold;
