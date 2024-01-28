from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.models import Base
import models.crud as crud
import models.schemas as schemas
from models.database import SessionLocal, engine
from utils.nvi import verify_tc_kimlik
from utils.mail import send_mail

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/ils/", response_model=List[schemas.Il])
def read_ils(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ils = crud.get_ils(db, skip=skip, limit=limit)
    return ils


@app.get("/api/ilces/", response_model=List[schemas.Ilce])
def read_ilces(il_id: int, db: Session = Depends(get_db)):
    ilces = crud.get_ilces_by_il_id(db, il_id)
    return ilces


@app.get("/api/muhtarliks/", response_model=List[schemas.Muhtarlik])
def read_muhtarliks(ilce_id: int, db: Session = Depends(get_db)):
    muhtarlix = crud.get_muhtarliks_by_ilce_id(db, ilce_id)
    return muhtarlix


@app.post("/api/musahit/", )
def add_musahit(musahit: schemas.MusahitBase, db: Session = Depends(get_db)):
    if not verify_tc_kimlik(musahit):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid TC Kimlik No"
        )
    try:
        musahit = crud.add_musahit_data(db, musahit)
        send_mail(musahit)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already Existing TC Kimlik No"
        )
    return musahit
