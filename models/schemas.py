from typing import Optional
from pydantic import BaseModel, EmailStr


class MusahitBase(BaseModel):
    tc_no: str
    first_name: str
    last_name: str

    dob: str
    sex: str
    mobile: str
    mail: EmailStr

    education: Optional[str] = None
    profession: Optional[str] = None
    extra: Optional[str] = None

    il_id: int
    ilce_id: int
    muhtarlik_id: int


class MuhtarlikBase(BaseModel):
    name: str


class Muhtarlik(MuhtarlikBase):
    id: int
    ilce_id: int
    il_id: int

    class ConfigDict:
        from_attributes = True


class IlceBase(BaseModel):
    name: str


class Ilce(IlceBase):
    id: int
    il_id: int
    # muhtarliklar: List[Muhtarlik] = []

    class ConfigDict:
        from_attributes = True


class IlBase(BaseModel):
    name: str


class Il(IlBase):
    id: int
    name: str
    # ilceler: List[Ilce] = []

    class ConfigDict:
        from_attributes = True
