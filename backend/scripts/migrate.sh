#!/bin/bash

# Stop on first error
set -e

# Parse arguments
nuke=false
message="database migration"

for arg in "$@"; do
    if [ "$arg" = "--nuke" ]; then
        nuke=true
    else
        message="$arg"
    fi
done

if [ "$nuke" = true ]; then
    echo -e "\033[31mNuking database...\033[0m"
    docker compose down -v
    echo -e "\033[31mRemoving all migrations...\033[0m"
    find api/alembic/versions/ -type f ! -name "__init__.py" -delete
fi

echo -e "\033[32mBuilding API container...\033[0m"
docker compose build api

echo -e "\033[32mCreating migration...\033[0m"
docker compose run --rm api alembic revision --autogenerate -m "$message"

echo -e "\033[32mApplying migration...\033[0m"
docker compose run --rm api alembic upgrade head

echo -e "\033[32mMigration complete!\033[0m" 