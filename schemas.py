from typing import List
from pydantic import BaseModel


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
