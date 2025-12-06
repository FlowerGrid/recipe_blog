# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_PATH = os.path.join(BASE_DIR, 'recipe-db.sqlite3')
DEFAULT_DATABASE_URL = f"sqlite:///{DB_PATH}"
DATABASE_URL = os.environ.get('DATABASE_URL', DEFAULT_DATABASE_URL)

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

print('db-url')
print(engine.url)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)

# Create a Session instance to use
db_session = SessionLocal()

# Create tables if they don't exist (optional, since Alembic should manage this in production)
Base.metadata.create_all(engine)
