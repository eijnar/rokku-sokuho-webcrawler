from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Band(Base):
    __tablename__ = 'band'  # Typically, table names are plural
    band_id = Column(Integer, primary_key=True, index=True)
    band_name = Column(String, nullable=False)

    # Relationship to BandURL, specifying cascade behaviors can be useful
    urls = relationship("BandURL", back_populates="band", cascade="all, delete-orphan")

class BandURL(Base):
    __tablename__ = 'band_url'  # Consistently using plural for table names
    url_id = Column(Integer, primary_key=True, index=True)
    band_id = Column(Integer, ForeignKey('band.band_id'), nullable=False)  # Ensure ForeignKey matches the table name
    url = Column(String, nullable=False)
    hash_value = Column(String)  # Consider if this needs to be indexed or has size limits
    date_added = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now())
    class_name = Column(String)
    last_failed = Column(DateTime)

    # Relationship to Band
    band = relationship("Band", back_populates="urls")
