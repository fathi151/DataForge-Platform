# PowerShell script to create airflow database in local PostgreSQL

$pgUser = "postgres"
$pgPassword = "postgres"  # Change this to your PostgreSQL password if different
$pgHost = "localhost"
$pgPort = "5432"

# Set environment variable for password
$env:PGPASSWORD = $pgPassword

Write-Host "Creating airflow database in PostgreSQL..."
Write-Host "Host: $pgHost"
Write-Host "Port: $pgPort"
Write-Host ""

# Create the airflow database
psql -h $pgHost -p $pgPort -U $pgUser -c "CREATE DATABASE airflow;"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Airflow database created successfully!"
} else {
    Write-Host "✗ Failed to create airflow database"
    Write-Host "The database might already exist, which is fine."
}

# Verify the database exists
Write-Host ""
Write-Host "Verifying databases..."
psql -h $pgHost -p $pgPort -U $pgUser -c "\l"

# Clean up
$env:PGPASSWORD = ""

Write-Host ""
Write-Host "Done! You can now start Airflow with: docker-compose up -d airflow-webserver"
