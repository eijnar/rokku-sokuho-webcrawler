from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ...models import Band as DB_Band
from ...dependencies import get_db
from ...schemas import Band, BandCreate, BandUpdate
from ..crud import create_band, update_band, delete_band

router = APIRouter()

@router.post("/bands/", response_model=Band)
def create_band_api(band: BandCreate, db: Session = Depends(get_db)):
    return create_band(db, band)

@router.get("/bands/", response_model=List[Band])
def read_bands(db: Session = Depends(get_db)):
    return db.query(DB_Band).all()

@router.put("/bands/{band_id}", response_model=Band)
def update_band_api(band_id: int, band: BandUpdate, db: Session = Depends(get_db)):
    return update_band(db, band_id, band)

@router.delete("/bands/{band_id}", status_code=204)
def delete_band_api(band_id: int, db: Session = Depends(get_db)):
    return delete_band(db, band_id)
