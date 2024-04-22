from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Base model for URL serialization and creation
class URLBase(BaseModel):
    url: str
    class_name: Optional[str] = None
    date_added: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    last_failed: Optional[datetime] = None

    class Config:
        orm_mode = True

# For creating a new URL, include the band_id that is not part of the base model
class URLCreate(URLBase):
    band_id: int

# For updating an existing URL, allow optional updates to url, class_name, and last_failed
class URLUpdate(BaseModel):
    url: Optional[str] = None
    class_name: Optional[str] = None
    last_failed: Optional[datetime] = None

# For displaying a URL, include all fields from URLBase plus the identifier fields
class URLDisplay(URLBase):
    url_id: int
    band_id: int

# Base model for bands
class BandBase(BaseModel):
    band_name: str

# Schema for creating a band (inherits BandBase and potentially adds other fields)
class BandCreate(BandBase):
    pass  # Use pass if no additional fields are required for creation

# Schema for updating a band, allowing optional updates to the band's name
class BandUpdate(BaseModel):
    band_name: Optional[str] = None

# Full Band schema for output, including a list of URLs
class Band(BaseModel):
    band_id: int
    band_name: str
    urls: Optional[List[URLDisplay]]  # Use URLDisplay for full URL details

    class Config:
        orm_mode = True
