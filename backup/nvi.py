try:
    from suds.client import Client
except ModuleNotFoundError:
    try:
        import subprocess
        subprocess.check_call(["pip", "install", "suds-py3==1.4.5.0"])
        from suds.client import Client
    except Exception as e:
        print(f"Error installing or importing suds-py3: {e}")
        exit(1)

client = Client("https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL")

def verification(params):
    try:
        return client.service.TCKimlikNoDogrula(**params)
    except Exception as e:
        return str(e)

args = {
            "TCKimlikNo": int(verificated_citizen_number),
            "Ad": verificated_name,
            "Soyad": verificated_surname,
            "DogumYili": int(verificated_birth_year)
        }
        response = verification(args)
        if response  == True:
                values.update({'verificated_name': values.get('name')})
                partner = request.env['res.partner'].sudo().search([('verificated_citizen_number', '=', verificated_citizen_number)])
                if partner:
                    raise UserError('Bu kimlik bilgileriyle daha önce bir kayıt oluşturulmuştur.')
                else:
                    return values
       
        else:
            raise UserError('Kimlik Bilgileriniz Sistemle Eşleşmemektedir.Lütfen tekrar kontrol ederek giriniz.')

