from sqlalchemy import create_engine
from constants.constants import SQLALCHEMY_DATABASE_URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database setup
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
  autocommit=False, 
  autoflush=False, 
  bind=engine
)
Base = declarative_base()

Base.metadata.create_all(bind=engine)