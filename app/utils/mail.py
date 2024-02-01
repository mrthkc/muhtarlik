import ssl
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

from config import Settings
from models.models import Musahit


def send_mail(musahit: Musahit):
    host = Settings().smtp_host
    port = Settings().smtp_port
    password = Settings().smtp_pass
    sender_email = Settings().sender_mail
    recipient_email = musahit.mail
    first_name = musahit.first_name
    last_name = musahit.last_name

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    subject = "Müşahit / Sandık Kurulu Üyesi / Gönüllü Başvurunuz Alındı"
    body = f"Sayın {first_name} {last_name},\n\nMüşahit / Sandık Kurulu Üyesi / Gönüllü başvurunuz kaydedilmiştir.\nİl / İlçe örgütümüz sizinle en kısa zamanda iletişime geçecektir.\n\nSevgiler,\nTürkiye İşçi Partisi"
    message = MIMEText(body, 'plain', 'utf-8')
    message['Subject'] = subject
    message['From'] = formataddr(
        (str(Header('Türkiye İşçi Partisi', 'utf-8')), sender_email)
    )
    message['To'] = recipient_email

    server = None
    try:
        server = smtplib.SMTP(host, port, timeout=60)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message.as_string())

    except Exception:
        pass

    if server:
        server.quit()
