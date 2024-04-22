# app/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...dependencies import get_db
from ...schemas import URLDisplay, URLCreate, URLUpdate
from ..crud import create_url, get_urls, update_url, delete_url

router = APIRouter()

@router.post("/urls/", response_model=URLDisplay)
def create_url_api(url: URLCreate, db: Session = Depends(get_db)):
    return create_url(db, url)

@router.get("/urls/", response_model=List[URLDisplay])
def read_urls(db: Session = Depends(get_db)):
    return get_urls(db)

@router.put("/urls/{url_id}", response_model=URLDisplay)
def update_url_api(url_id: int, url: URLUpdate, db: Session = Depends(get_db)):
    return update_url(db, url_id, url)

@router.delete("/urls/{url_id}", status_code=204)
def delete_url_api(url_id: int, db: Session = Depends(get_db)):
    return delete_url(db, url_id)
