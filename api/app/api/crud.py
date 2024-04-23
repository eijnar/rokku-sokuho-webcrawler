from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import Band, BandURL
from ..schemas import BandCreate, BandUpdate, URLCreate, URLUpdate


def create_band(db: Session, band_data: BandCreate):
    # Create an instance of the Band model
    new_band = Band(band_name=band_data.band_name)
    db.add(new_band)
    db.commit()
    db.refresh(new_band)
    return new_band


def get_bands(db: Session):
    # Retrieve all bands
    return db.query(Band).all()


def update_band(db: Session, band_id: int, band_data: BandUpdate):
    # Find the existing band
    band = db.query(Band).filter(Band.band_id == band_id).first()
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")

    # Update the band details
    if band_data.band_name is not None:
        band.band_name = band_data.band_name
    db.commit()
    return band


def delete_band(db: Session, band_id: int):
    # Find the band and delete it
    band = db.query(Band).filter(Band.band_id == band_id).first()
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")

    db.delete(band)
    db.commit()


def create_url(db: Session, url_data: URLCreate):
    new_url = BandURL(**url_data.dict())
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url


def get_urls(db: Session):
    return db.query(BandURL).all()


def get_urls_by_band_id(db: Session, band_id: int):
    return db.query(BandURL).filter(BandURL.band_id == band_id).all()


def update_url(db: Session, url_id: int, url_data: URLUpdate):
    url = db.query(BandURL).filter(BandURL.url_id == url_id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url.url = url_data.url if url_data.url is not None else url.url
    url.class_name = url_data.class_name if url_data.class_name is not None else url.class_name
    url.last_failed = url_data.last_failed if url_data.last_failed is not None else url.last_failed
    db.commit()
    return url


def delete_url(db: Session, url_id: int):
    url = db.query(BandURL).filter(BandURL.url_id == url_id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(url)
    db.commit()
