import logging
import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.crm import send_lead_to_crm
from src.emails import send_email_about_new_client
from src.sheets import insert_new_row

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ROOT_DIRECTORY = Path(__file__).resolve().parent.parent
TEMPLATES_DIRECTORY = ROOT_DIRECTORY / "templates"
root = Jinja2Templates(str(TEMPLATES_DIRECTORY))

from pydantic import BaseModel, field_validator
import re

from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings


# Модель для заявки
class ApplicationRequest(BaseModel):
    name: str
    email: str
    tel: str
    child_age: str
    is_policy_accepted: str

    @field_validator('name')
    def validate_name(cls, v):
        v = v.strip()
        if len(v) < 2 or len(v) > 50:
            raise ValueError('Имя должно быть от 2 до 50 символов')
        if not re.fullmatch(r'^[A-Za-zА-Яа-яЁё\s\-\']+$', v):
            raise ValueError('Имя может содержать только буквы, пробелы и дефисы')
        return v

    @field_validator('tel')
    def validate_phone(cls, v):
        digits = re.sub(r'\D', '', v)
        if len(digits) < 5 or len(digits) > 15:
            raise ValueError('Телефон должен содержать от 5 до 15 цифр')
        return digits

    @field_validator('email')
    def validate_email(cls, v):
        v = v.strip().lower()
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', v):
            raise ValueError('Введите корректный email адрес')
        if len(v) > 100:
            raise ValueError('Email слишком длинный')
        return v

    @field_validator('child_age')
    def validate_child_age(cls, v):
        ALLOWED_AGES = {'7-9', '10-12', '13-15', '16-17'}
        if v not in ALLOWED_AGES:
            raise ValueError('Выбран недопустимый возраст')
        return v

    @field_validator('is_policy_accepted')
    def validate_policy(cls, v):
        accepted_values = {'true', '1', 'yes', 'да'}
        if v.lower() not in accepted_values and v is not True:
            raise ValueError('Необходимо согласие с политикой конфиденциальности')
        return v


def make_up():
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )

    class CsrfSettings(BaseSettings):
        secret_key: str
        csrf_token_location: str = "form"
        cookie_samesite: str = "lax"
        cookie_secure: bool = True

        class Config:
            env_prefix = "CSRF_"  # Автоматически найдет CSRF_SECRET_KEY

    @CsrfProtect.load_config
    def get_csrf_config():
        return CsrfSettings()

    # Обработчик ошибок CSRF
    @app.exception_handler(CsrfProtectError)
    def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

    static_path = os.path.join(ROOT_DIRECTORY, "static")
    app.mount("/app/static", StaticFiles(directory=str(static_path)), name="static")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def index(request: Request, csrf_protect: CsrfProtect = Depends()):
        # Генерация токенов
        csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
        # Создание ответа с шаблоном
        response = root.TemplateResponse("base.html", {"request": request, "csrf_token": csrf_token})
        # Установка подписанного токена в cookie
        csrf_protect.set_csrf_cookie(signed_token, response)
        return response

    @app.get("/thank-you")
    async def thank_you(request: Request):
        return root.TemplateResponse("thank_you.html", {"request": request})

    @app.get("/offer")
    async def offer_page(request: Request):
        return root.TemplateResponse("offer.html", {"request": request})

    @app.get("/privacy")
    async def privacy_policy(request: Request):
        return root.TemplateResponse("privacy.html", {"request": request})

    # @app.get("/advertising")
    # async def privacy_policy(request: Request):
    #     return root.TemplateResponse("templates/advertising.html", {"request": request})

    @app.get("/sitemap.xml")
    async def sitemap():
        sitemap_path = ROOT_DIRECTORY / "static" / "sitemap.xml"
        return FileResponse(str(sitemap_path), media_type="application/xml")

    @app.get("/courses.xml", include_in_schema=False)
    async def courses_feed():
        courses_path = ROOT_DIRECTORY / "static" / "courses.xml"
        return FileResponse(str(courses_path), media_type="application/xml")

    @app.get("/robots.txt")
    async def robots():
        robots_path = ROOT_DIRECTORY / "static" / "robots.txt"
        return FileResponse(str(robots_path), media_type="text/plain")

    # пути к файлам которые далее лучше заменить на alias настройках nginx чтобы не нагружать Fast Api, будет быстрее
    @app.get('/favicon.ico', include_in_schema=False)
    async def favicon():
        path = ROOT_DIRECTORY / "static" / "icons" / "favicon.ico"
        return FileResponse(path)

    @app.get('/apple-touch-icon.png', include_in_schema=False)
    async def apple_touch_icon():
        path = ROOT_DIRECTORY / "static" / "icons" / "apple-touch-icon.png"
        return FileResponse(path)

    @app.get('/favicon-16x16.png', include_in_schema=False)
    async def favicon_16():
        path = ROOT_DIRECTORY / "static" / "icons" / "favicon-16x16.png"
        return FileResponse(path)

    @app.get('/favicon-32x32.png', include_in_schema=False)
    async def favicon_32():
        path = ROOT_DIRECTORY / "static" / "icons" / "favicon-32x32.png"
        return FileResponse(path)

    @app.get('/android-chrome-192x192.png', include_in_schema=False)
    async def android_192():
        path = ROOT_DIRECTORY / "static" / "icons" / "android-chrome-192x192.png"
        return FileResponse(path)

    @app.get('/android-chrome-512x512.png', include_in_schema=False)
    async def android_512():
        path = ROOT_DIRECTORY / "static" / "icons" / "android-chrome-512x512.png"
        return FileResponse(path)

    def send_email_background(message):
        try:
            result = send_email_about_new_client(message)
            if result:
                pass
            else:
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
            logger.error("❌ Фоновая запись в таблицу не удалась")

    import asyncio

    @app.post("/request/")
    @app.post("/request")
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

        logger.info(f"✅ Валидная заявка от {request_data.name}")

        message = f"{request_data.name} [Возраст: {request_data.child_age}]\n📞 {request_data.tel} ✉ {request_data.email}"

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
            "message": f"Уважаемый(ая) {name},\nМы рады сообщить, что ваша заявка принята! Менеджер свяжется с вами в ближайшее время.\n\nС уважением,\nKodama"
        }

    return app


app = make_up()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5050, reload=True)
