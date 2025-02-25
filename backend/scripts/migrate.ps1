# Stop on first error
$ErrorActionPreference = "Stop"

Write-Host "Building API container..." -ForegroundColor Green
docker-compose build api

Write-Host "Creating migration..." -ForegroundColor Green
docker-compose run --rm api alembic revision --autogenerate -m $args[0]

Write-Host "Applying migration..." -ForegroundColor Green
docker-compose run --rm api alembic upgrade head

Write-Host "Migration complete!" -ForegroundColor Green 