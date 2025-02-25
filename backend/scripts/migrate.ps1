# Stop on first error
$ErrorActionPreference = "Stop"

# Check for --nuke flag
$nuke = $false
$message = "database migration"

foreach ($arg in $args) {
    if ($arg -eq "--nuke") {
        $nuke = $true
    } else {
        $message = $arg
    }
}

if ($nuke) {
    Write-Host "Nuking database..." -ForegroundColor Red
    docker compose down -v
    Write-Host "Removing all migrations..." -ForegroundColor Red
    Get-ChildItem -Path "api/alembic/versions/" -Exclude "__init__.py" | Remove-Item -Force
}

Write-Host "Building API container..." -ForegroundColor Green
docker-compose build api

Write-Host "Creating migration..." -ForegroundColor Green
docker-compose run --rm api alembic revision --autogenerate -m $message

Write-Host "Applying migration..." -ForegroundColor Green
docker-compose run --rm api alembic upgrade head

Write-Host "Migration complete!" -ForegroundColor Green 