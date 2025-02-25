#!/bin/bash

# Stop on first error
set -e

echo "Building API container..."
docker-compose build api

echo "Creating migration..."
docker-compose run --rm api alembic revision --autogenerate -m "$1"

echo "Applying migration..."
docker-compose run --rm api alembic upgrade head

echo "Migration complete!" 