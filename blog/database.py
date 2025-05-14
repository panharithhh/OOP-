# blog/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Tell SQLAlchemy where your database lives:
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# 2. Create an “engine” that knows how to talk to that database.
#    For SQLite we also pass `check_same_thread=False` so multiple
#    parts of FastAPI can share one connection safely.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 3. sessionmaker() lets you create “sessions” (think of them like
#    individual conversations with the database).
#    We disable auto-commit/auto-flush so you control when data is saved.
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# 4. Base class for all your ORM models.
#    You’ll subclass this to define tables (e.g. a BlogPost model).
Base = declarative_base()

