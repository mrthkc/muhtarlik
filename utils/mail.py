import ssl
import smtplib
from fastapi import HTTPException, status
import traceback

from config import Settings
from models.models import Musahit


def send_mail(musahit: Musahit):
    host = Settings().smtp_host
    port = Settings().smtp_port
    password = Settings().smtp_pass
    sender_email = Settings().sender_mail

    print(host, port, password, sender_email)

    context = ssl.create_default_context()

    message = """\
Subject: Müşahit / Sandık Kurulu Üyesi Başvurunuz Alındı

    Değerli {} {},
Müşahit / Sandık kurulu üyesi başvurunuz kaydedilmiştir.

Sevgiler.
Türkiye İşçi Partisi
""".format(musahit.first_name, musahit.last_name).encode('utf-8')

    server = None
    try:
        server = smtplib.SMTP(host=host, port=port, timeout=60)
        server.ehlo()
        server.starttls(context=context)  # Secure
        server.ehlo()
        server.login(user=sender_email, password=password)

        # send mail
        server.sendmail(
            from_addr=sender_email,
            to_addrs=musahit.mail,
            msg=message
        )

    except Exception as e:
        print(e)
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="sending mail error"
        )
    finally:
        if server:
            server.quit()
