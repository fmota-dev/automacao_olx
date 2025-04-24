import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_ad_email(title, price, link):
    remetente = "fmota.web@gmail.com"
    destinatario = "filipe.motasl@outlook.com"
    senha = "zdar nmds rgny mqqk"

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = "Novo anúncio encontrado na OLX"

    corpo = f"""
    🚗 Novo anúncio encontrado:

    🏷️ Título: {title}
    💰 Preço: {price}
    🔗 Link: {link}
    """

    msg.attach(MIMEText(corpo, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
