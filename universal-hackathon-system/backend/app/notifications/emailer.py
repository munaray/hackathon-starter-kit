import smtplib
from email.mime.text import MIMEText
from ..config import settings


def send_email(to_email: str, subject: str, body: str):
    if not settings.smtp_host or not settings.smtp_port:
        raise RuntimeError("SMTP not configured")
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from or "no-reply@example.com"
    msg["To"] = to_email

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        if settings.smtp_user and settings.smtp_password:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(msg["From"], [to_email], msg.as_string())