from sqlalchemy.orm import Session

from models.models import (
    Il, Ilce, Muhtarlik, Musahit
)
import models.schemas as schemas


def get_ils(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Il).offset(skip).limit(limit).all()


def get_ilces_by_il_id(db: Session, il_id: int):
    return db.query(Ilce).filter(
        Ilce.il_id == il_id
    ).all()


def get_muhtarliks_by_ilce_id(db: Session, ilce_id: int):
    return db.query(Muhtarlik).filter(
        Muhtarlik.ilce_id == ilce_id
    ).all()


def add_musahit_data(db: Session, musahit: schemas.MusahitBase):
    musahit = Musahit(**musahit.model_dump())
    db.add(musahit)
    db.commit()
    db.refresh(musahit)

    return musahit
