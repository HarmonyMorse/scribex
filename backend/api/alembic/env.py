from alembic import context
from app.core.config import settings
from app.models.base import Base
from app.models.user import User

# Tell Alembic what your tables look like
target_metadata = Base.metadata

# Tell Alembic how to connect to your database
config = context.config
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

# Run the migration
with context.begin_transaction():
    context.run_migrations()