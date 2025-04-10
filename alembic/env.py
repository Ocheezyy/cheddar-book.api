import sys
import os
from logging.config import fileConfig
from sqlmodel import SQLModel
from alembic import context
from dotenv import load_dotenv

# Load .env before anything
load_dotenv()

# Add your app folder to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import engine
from app.db import models

# Alembic Config object
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Target metadata (SQLModel uses metadata from all models)
target_metadata = SQLModel.metadata


def run_migrations_offline():
    context.configure(
        url=os.getenv("DATABASE_URL"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
