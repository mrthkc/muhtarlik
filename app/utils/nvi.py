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


def verify_tc_kimlik_algorithm(value):
    """
    Kurallar:
    * 11 hanelidir.
    * Her hanesi rakamsal değer içerir.
    * İlk hane 0 olamaz.
    * 1. 3. 5. 7. ve 9. hanelerin toplamının 7 katından, 2. 4. 6. ve 8. hanelerin toplamı çıkartıldığında, elde edilen sonucun 10'a bölümünden kalan, yani Mod10'u bize 10. haneyi verir.
    * 1. 2. 3. 4. 5. 6. 7. 8. 9. ve 10. hanelerin toplamından elde edilen sonucun 10'a bölümünden kalan, yani Mod10'u bize 11. haneyi verir.
    Kurallar http://www.kodaman.org/yazi/t-c-kimlik-no-algoritmasi adresinden alınmıştır.
    """
    value = str(value)

    # 11 hanelidir.
    if not len(value) == 11:
        return False

    # Sadece rakamlardan olusur.
    if not value.isdigit():
        return False

    # Ilk hanesi 0 olamaz.
    if int(value[0]) == 0:
        return False

    digits = [int(d) for d in str(value)]

    # 1. 2. 3. 4. 5. 6. 7. 8. 9. ve 10. hanelerin toplamından elde edilen sonucun
    # 10'a bölümünden kalan, yani Mod10'u bize 11. haneyi verir.
    if not sum(digits[:10]) % 10 == digits[10]:
        print("mert1")
        return False

    # 1. 3. 5. 7. ve 9. hanelerin toplamının 7 katından, 2. 4. 6. ve 8. hanelerin toplamı çıkartıldığında,
    # elde edilen sonucun 10'a bölümünden kalan, yani Mod10'u bize 10. haneyi verir.
    if not (((7 * sum(digits[:9][-1::-2])) - sum(digits[:9][-2::-2])) % 10) == digits[9]:
        print("mert2")
        return False

    # Butun kontrollerden gecti.
    return True
