from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from database import Base


class Il(Base):
    __tablename__ = "il"

    id = mapped_column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    ilceler = relationship("Ilce", back_populates="il")
    muhtarliklar = relationship("Muhtarlik", back_populates="il")


class Ilce(Base):
    __tablename__ = "ilce"

    id = mapped_column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    il_id = mapped_column(ForeignKey("il.id"))

    il = relationship("Il", back_populates="ilceler")
    muhtarliklar = relationship("Muhtarlik", back_populates="ilce")


class Muhtarlik(Base):
    __tablename__ = "muhtarlik"

    id = mapped_column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    il_id = mapped_column(ForeignKey("il.id"))
    ilce_id = mapped_column(ForeignKey("ilce.id"))

    il = relationship("Il", back_populates="muhtarliklar")
    ilce = relationship("Ilce", back_populates="muhtarliklar")
