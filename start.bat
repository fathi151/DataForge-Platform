@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo Data Platform - Starting Services
echo ==========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

echo Starting Docker containers...
docker-compose up -d

echo.
echo Waiting for services to be ready...
timeout /t 10 /nobreak

echo.
echo ==========================================
echo Services are starting up!
echo ==========================================
echo.
echo Access the following services:
echo.
echo 1. Airflow (Orchestration)
echo    URL: http://localhost:8080
echo    Username: admin
echo    Password: admin
echo.
echo 2. Grafana (Visualization)
echo    URL: http://localhost:3000
echo    Username: admin
echo    Password: admin
echo.
echo 3. Jupyter (Data Analysis)
echo    URL: http://localhost:8888
echo.
echo 4. Adminer (Database Management)
echo    URL: http://localhost:8081
echo    Server: postgres
echo    Username: datauser
echo    Password: datapass123
echo    Database: datawarehouse
echo.
echo 5. MinIO (Object Storage)
echo    URL: http://localhost:9001
echo    Username: minioadmin
echo    Password: minioadmin123
echo.
echo 6. Redis (Caching)
echo    Host: localhost:6379
echo.
echo ==========================================
echo.
echo To view logs:
echo   docker-compose logs -f [service_name]
echo.
echo To stop services:
echo   docker-compose down
echo.
echo To load sample data:
echo   docker-compose exec postgres python /scripts/load_sample_data.py
echo.
pause
