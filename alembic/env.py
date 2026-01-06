import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# -------------------------------------------------
# Make sure /app is on PYTHONPATH
# -------------------------------------------------
sys.path.append("/app")

# -------------------------------------------------
# Alembic config
# -------------------------------------------------
config = context.config

# Apply logging config from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -------------------------------------------------
# Override sqlalchemy.url with environment variable
# -------------------------------------------------
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL is not set in environment")
config.set_main_option("sqlalchemy.url", database_url)

# -------------------------------------------------
# Import your Base and models (critical for autogenerate)
# -------------------------------------------------
from app.models.base import Base
from app.models.users import User
from app.models.products import Products
from app.models.stock import Stocks

target_metadata = Base.metadata

# -------------------------------------------------
# Offline migrations
# -------------------------------------------------
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# -------------------------------------------------
# Online migrations
# -------------------------------------------------
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Detect column type changes
        )
        with context.begin_transaction():
            context.run_migrations()

# -------------------------------------------------
# Run migrations
# -------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
