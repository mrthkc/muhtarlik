from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from models.database import Base


class Il(Base):
    __tablename__ = "il"

    id = mapped_column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    ilceler = relationship("Ilce", back_populates="il")
    muhtarliklar = relationship("Muhtarlik", back_populates="il")
    musahitler = relationship("Musahit", back_populates="il")


class Ilce(Base):
    __tablename__ = "ilce"

    id = mapped_column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    il_id = mapped_column(ForeignKey("il.id"))

    il = relationship("Il", back_populates="ilceler")
    muhtarliklar = relationship("Muhtarlik", back_populates="ilce")
    musahitler = relationship("Musahit", back_populates="ilce")


class Muhtarlik(Base):
    __tablename__ = "muhtarlik"

    id = mapped_column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    il_id = mapped_column(ForeignKey("il.id"))
    ilce_id = mapped_column(ForeignKey("ilce.id"))

    il = relationship("Il", back_populates="muhtarliklar")
    ilce = relationship("Ilce", back_populates="muhtarliklar")
    musahitler = relationship("Musahit", back_populates="muhtarliklar")


class Musahit(Base):
    __tablename__ = "musahit"

    id = mapped_column(Integer, primary_key=True)
    tc_no = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    dob = Column(Date, nullable=False)
    sex = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    mail = Column(String, nullable=False)

    education = Column(String, nullable=True)
    profession = Column(String, nullable=True)
    extra = Column(String, nullable=True)

    il_id = mapped_column(ForeignKey("il.id"))
    ilce_id = mapped_column(ForeignKey("ilce.id"))
    muhtarlik_id = mapped_column(ForeignKey("muhtarlik.id"))

    il = relationship("Il", back_populates="musahitler")
    ilce = relationship("Ilce", back_populates="musahitler")
    muhtarliklar = relationship("Muhtarlik", back_populates="musahitler")

    __table_args__ = (
        UniqueConstraint('tc_no', name='_tc_kimlik_uc'),
        UniqueConstraint('mail', name='_mail_uc'),
        UniqueConstraint('mobile', name='_mobile_uc'),
    )
