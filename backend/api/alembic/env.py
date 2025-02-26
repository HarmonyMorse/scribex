from alembic import context
from app.core.config import settings
from app.models import *  # This imports all models defined in __init__.py
from sqlalchemy import create_engine

# Tell Alembic what your tables look like
target_metadata = Base.metadata

# Tell Alembic how to connect to your database
config = context.config
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(str(settings.DATABASE_URL))

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    raise Exception("Offline mode not supported")
else:
    run_migrations_online()