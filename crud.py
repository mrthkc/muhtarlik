from sqlalchemy.orm import Session

import models
import schemas


def get_ils(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Il).offset(skip).limit(limit).all()


def get_ilces_by_il_id(db: Session, il_id: int):
    return db.query(models.Ilce).filter(
        models.Ilce.il_id == il_id
    ).all()


def get_muhtarliks_by_ilce_id(db: Session, ilce_id: int):
    return db.query(models.Muhtarlik).filter(
        models.Muhtarlik.ilce_id == ilce_id
    ).all()


def add_musahit_data(db: Session, musahit: schemas.MusahitBase):
    musahit = models.Musahit(**musahit.model_dump())
    db.add(musahit)
    db.commit()
    db.refresh(musahit)

    return musahit
