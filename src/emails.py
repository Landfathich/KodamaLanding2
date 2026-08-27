import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "kodama.edu@gmail.com"
TO_EMAIL = "landfathich@gmail.com"

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email_about_new_client(body: str = "") -> bool:
    if not EMAIL_PASSWORD:
        logger.error("❌ Пароль EMAIL_PASSWORD не задан в .env")
        return False

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = "Новая заявка на сайте!"

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Шифруем соединение
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, TO_EMAIL, msg.as_string())
        logger.info("✅ Письмо успешно отправлено!")
        return True
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"❌ Ошибка аутентификации: неверный логин или пароль: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке письма: {e}")
        return False
