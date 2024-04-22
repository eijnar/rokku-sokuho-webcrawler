from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy database URL
DATABASE_URL = "postgresql://webcrawler:XSnqTFv3pHSb2VTUWAY8Vg@172.30.149.76/webcrawler"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

# SessionLocal class, which will be a factory for creating new Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our classes definitions
Base = declarative_base()
