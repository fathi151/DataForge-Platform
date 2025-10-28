@echo off
REM Setup script for local PostgreSQL configuration
REM This script creates the necessary databases and users for Airflow

echo ========================================
echo PostgreSQL Local Setup
echo ========================================
echo.
echo This script will create the required databases and users.
echo Make sure PostgreSQL is running on localhost:5432
echo.

REM Check if psql is available
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: psql command not found. 
    echo Please ensure PostgreSQL is installed and added to PATH.
    echo.
    echo You can manually run the setup-local-postgres.sql file using:
    echo   psql -U postgres -f setup-local-postgres.sql
    pause
    exit /b 1
)

echo Running PostgreSQL setup script...
echo.

REM Run the SQL script
psql -U postgres -f setup-local-postgres.sql

if %ERRORLEVEL% EQ 0 (
    echo.
    echo ========================================
    echo Setup completed successfully!
    echo ========================================
    echo.
    echo Your PostgreSQL is now configured with:
    echo   - Database: airflow
    echo   - Database: datawarehouse
    echo   - User: datauser
    echo   - Password: datapass123
    echo.
    echo You can now start the Docker containers with:
    echo   docker-compose up -d
    echo.
) else (
    echo.
    echo Error: Setup failed. Please check your PostgreSQL installation.
    echo.
)

pause
