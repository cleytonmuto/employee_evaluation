# app/crud/sector.py
from sqlalchemy.orm import Session
from app.models.sector import Sector

def create_sector(db: Session, name: str, description: str | None = None) -> Sector:
    s = Sector(name=name, description=description)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

def list_sectors(db: Session):
    return db.query(Sector).all()

def get_sector(db: Session, sector_id):
    return db.query(Sector).filter(Sector.id == sector_id).first()
