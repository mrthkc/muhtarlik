from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/ils/", response_model=List[schemas.Il])
def read_ils(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ils = crud.get_ils(db, skip=skip, limit=limit)
    return ils


@app.get("/ilces/", response_model=List[schemas.Ilce])
def read_ilces(il_id: int, db: Session = Depends(get_db)):
    ilces = crud.get_ilces_by_il_id(db, il_id)
    return ilces


@app.get("/muhtarliks/", response_model=List[schemas.Muhtarlik])
def read_muhtarliks(ilce_id: int, db: Session = Depends(get_db)):
    muhtarlix = crud.get_muhtarliks_by_ilce_id(db, ilce_id)
    return muhtarlix
