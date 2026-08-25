import os
import logging
import httpx

logger = logging.getLogger(__name__)

CRM_URL = os.getenv("CRM_URL")
CRM_API_KEY = os.getenv("CRM_API_KEY")

async def send_lead_to_crm(name: str, phone: str, email: str, course: str, source_url: str = ""):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                CRM_URL,
                json={
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "course": course,
                    "source": "landing",
                    "source_url": source_url
                },
                headers={"X-API-Key": CRM_API_KEY}
            )
            if response.status_code == 201:
                logger.info(f"Лидер в CRM: {name}")
            else:
                logger.error(f"CRM ошибка {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Не удалось отправить в CRM: {e}")