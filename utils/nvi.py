from suds.client import Client

from models.schemas import MusahitBase


def verify_tc_kimlik(musahit: MusahitBase):
    client = Client("https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL")
    args = {
        "TCKimlikNo": int(musahit.tc_no),
        "Ad": musahit.first_name,
        "Soyad": musahit.last_name,
        "DogumYili": int(musahit.dob[:4])
    }

    return client.service.TCKimlikNoDogrula(**args)
