# app/api/v1/sectors.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.api.deps import get_current_user, require_admin
from app.schemas.sector import SectorCreate, SectorOut
from app.crud.sector import create_sector, list_sectors, get_sector

router = APIRouter()

@router.get("/", response_model=list[SectorOut])
def list_sectors_endpoint(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return list_sectors(db)

@router.post("/", response_model=SectorOut)
def create_sector_endpoint(payload: SectorCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return create_sector(db, payload.name, payload.description)

@router.get("/{sector_id}", response_model=SectorOut)
def get_sector_endpoint(sector_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    sector = get_sector(db, sector_id)
    if sector is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return sector
