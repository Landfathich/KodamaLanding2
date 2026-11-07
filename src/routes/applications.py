import asyncio
import logging
import re

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel, field_validator

from src.crm import send_lead_to_crm
from src.emails import send_email_about_new_client
from src.sheets import insert_new_row

logger = logging.getLogger(__name__)

router = APIRouter()


class ApplicationRequest(BaseModel):
    name: str
    email: str
    tel: str
    child_age: str
    is_policy_accepted: str

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if len(v) < 2 or len(v) > 50:
            raise ValueError("Имя должно быть от 2 до 50 символов")
        if not re.fullmatch(r"^[A-Za-zА-Яа-яЁё\s\-\']+$", v):
            raise ValueError("Имя может содержать только буквы, пробелы и дефисы")
        return v

    @field_validator("tel")
    def validate_phone(cls, v):
        digits = re.sub(r"\D", "", v)
        if len(digits) < 5 or len(digits) > 15:
            raise ValueError("Телефон должен содержать от 5 до 15 цифр")
        return digits

    @field_validator("email")
    def validate_email(cls, v):
        v = v.strip().lower()
        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", v):
            raise ValueError("Введите корректный email адрес")
        if len(v) > 100:
            raise ValueError("Email слишком длинный")
        return v

    @field_validator("child_age")
    def validate_child_age(cls, v):
        allowed_ages = {"6-9", "10-12", "13-17"}
        if v not in allowed_ages:
            raise ValueError("Выбран недопустимый возраст")
        return v

    @field_validator("is_policy_accepted")
    def validate_policy(cls, v):
        accepted_values = {"true", "1", "yes", "да"}
        if v.lower() not in accepted_values and v is not True:
            raise ValueError("Необходимо согласие с политикой конфиденциальности")
        return v


def send_email_background(message):
    try:
        result = send_email_about_new_client(message)
        if not result:
            logger.error("Фоновая отправка email не удалась")
    except Exception as e:
        logger.error(f"Критическая ошибка при отправке email: {e}")


def insert_row_background(email, tel, child_age, name, is_policy_accepted):
    result = insert_new_row(
        mail=email,
        phone=tel,
        child_age=child_age,
        name=name,
        is_policy_accepted=is_policy_accepted,
        comment="Заявка принята"
    )
    if result:
        logger.info("Google Sheets обновлен в фоне")
    else:
        logger.error("Фоновая запись в таблицу не удалась")


@router.post("/request/")
@router.post("/request")
async def post_request(
        request: Request,
        csrf_protect: CsrfProtect = Depends(),
        name: str = Form(...),
        email: str = Form(...),
        tel: str = Form(...),
        child_age: str = Form(...),
        is_policy_accepted: str = Form(...)
):
    await csrf_protect.validate_csrf(request)

    try:
        request_data = ApplicationRequest(
            name=name,
            email=email,
            tel=tel,
            child_age=child_age,
            is_policy_accepted=is_policy_accepted
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    logger.info(f"Валидная заявка от {request_data.name}")

    message = (
        f"{request_data.name} [Возраст: {request_data.child_age}]\n"
        f"📞 {request_data.tel} ✉ {request_data.email}"
    )

    asyncio.create_task(asyncio.to_thread(send_email_background, message))

    asyncio.create_task(asyncio.to_thread(
        insert_row_background,
        email=request_data.email,
        tel=request_data.tel,
        child_age=request_data.child_age,
        name=request_data.name,
        is_policy_accepted=request_data.is_policy_accepted
    ))

    asyncio.create_task(send_lead_to_crm(
        name=request_data.name,
        phone=request_data.tel,
        email=request_data.email,
        child_age=request_data.child_age,
        source_url=request.headers.get("referer", "") or ""
    ))

    return {
        "status": "success",
        "message": (
            f"Уважаемый(ая) {name},\n"
            "Мы рады сообщить, что ваша заявка принята! "
            "Менеджер свяжется с вами в ближайшее время.\n\n"
            "С уважением,\nKodama"
        )
    }
