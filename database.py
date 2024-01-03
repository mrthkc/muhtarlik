from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Settings

settings = Settings()

SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@localhost:{}/{}'.format(
    settings.db_user,
    settings.db_pass,
    settings.db_port,
    settings.db_name,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
