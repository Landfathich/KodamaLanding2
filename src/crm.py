import logging
import os

import httpx

logger = logging.getLogger(__name__)

CRM_URL = os.getenv("CRM_URL")
CRM_API_KEY = os.getenv("CRM_API_KEY")


async def send_lead_to_crm(
    name: str,
    phone: str,
    email: str,
    child_age: str,
    source_url: str = "",
    utm_source: str = "",
    utm_medium: str = "",
    utm_campaign: str = "",
    utm_content: str = "",
    utm_term: str = "",
    ip_address: str = "",
    user_agent: str = "",
    page_url: str = "",
    accept_language: str = "",
    created_at: str = ""
):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                CRM_URL,
                json={
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "child_age": child_age,
                    "source": "landing",
                    "source_url": source_url,
                    "utm_source": utm_source,
                    "utm_medium": utm_medium,
                    "utm_campaign": utm_campaign,
                    "utm_content": utm_content,
                    "utm_term": utm_term,
                    "ip_address": ip_address,
                    "user_agent": user_agent,
                    "page_url": page_url,
                    "accept_language": accept_language,
                    "created_at": created_at
                },
                headers={"X-API-Key": CRM_API_KEY}
            )
            if response.status_code == 201:
                logger.info(f"✅ Лид в CRM: {name}")
            else:
                logger.error(f"❌ CRM ошибка {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"❌ Не удалось отправить в CRM: {e}")
