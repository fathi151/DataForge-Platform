@echo off
REM Create airflow database in local PostgreSQL

echo ========================================
echo Creating Airflow Database
echo ========================================
echo.

REM Check if psql is available
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: psql command not found.
    echo Please ensure PostgreSQL is installed and added to PATH.
    echo.
    echo You can manually create the database by running:
    echo   psql -U postgres -c "CREATE DATABASE airflow;"
    echo.
    pause
    exit /b 1
)

echo Creating airflow database...
psql -U postgres -c "CREATE DATABASE airflow;"

if %ERRORLEVEL% EQ 0 (
    echo.
    echo ✓ Airflow database created successfully!
) else (
    echo.
    echo Note: Database might already exist, which is fine.
)

echo.
echo Listing all databases:
psql -U postgres -c "\l"

echo.
echo ========================================
echo You can now start Airflow with:
echo   docker-compose up -d airflow-webserver
echo ========================================
echo.

pause
