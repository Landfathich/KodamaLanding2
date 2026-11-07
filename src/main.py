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
        ALLOWED_AGES = {'6-9', '10-12', '13-17'}
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
        csrf_token_location: str = "header"
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

    def render_page(request: Request, template_name: str, csrf_protect: CsrfProtect, context: dict = None):
        csrf_token, signed_token = csrf_protect.generate_csrf_tokens()

        template_context = {
            "request": request,
            "csrf_token": csrf_token,
            **(context or {})
        }

        response = root.TemplateResponse(template_name, template_context)
        csrf_protect.set_csrf_cookie(signed_token, response)

        return response

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
        return render_page(request, "index.html", csrf_protect)

    @app.get("/thank-you")
    async def thank_you(request: Request, csrf_protect: CsrfProtect = Depends()):
        return render_page(request, "thank_you.html", csrf_protect)

    @app.get("/courses")
    async def courses_page(request: Request, csrf_protect: CsrfProtect = Depends()):
        return render_page(request, "courses.html", csrf_protect)

    @app.get("/directions/programming")
    async def direction_programming(
            request: Request,
            csrf_protect: CsrfProtect = Depends()
    ):
        data = {
            "title": "Программирование",
            "direction_name": "Программирование",
            "accent": "#6E65FF",
            "hero_title": "Программирование для детей 6–17 лет",
            "hero_subtitle": "Учим писать код с нуля и развиваем логику. Индивидуальные онлайн-занятия с преподавателем — от первых игр на Scratch до Python, C++ и олимпиадных задач.",
            "image": "/images/direction_programming.webp",
            "image_position": "center",
            "learn": [
                {
                    "icon": "🎮",
                    "title": "Scratch — первые шаги",
                    "accent": "#FFC75C",
                    "text": "Ребёнок собирает игры и мультфильмы из блоков, осваивает логику и алгоритмы без сложного кода.",
                    "points": ["Логика и алгоритмы", "Анимация и события", "Основы программирования"]
                },
                {
                    "icon": "🐍",
                    "title": "Python — настоящий язык",
                    "accent": "#FFD54F",
                    "text": "От первых строк кода к реальным программам: боты, игры, сайты, работа с данными.",
                    "points": ["Синтаксис Python", "Telegram и Discord боты", "Django и сайты"]
                },
                {
                    "icon": "⚡",
                    "title": "C++ — мощный инструмент",
                    "accent": "#6E65FF",
                    "text": "Для тех, кто хочет серьёзно: 2D-игры, работа с памятью, алгоритмы.",
                    "points": ["Синтаксис C++", "2D-игры", "Алгоритмы"]
                },
                {
                    "icon": "🏆",
                    "title": "Олимпиады и алгоритмы",
                    "accent": "#E769E4",
                    "text": "Подготовка к олимпиадам по программированию: сложные задачи, структуры данных.",
                    "points": ["Алгоритмы", "Структуры данных", "Решение задач"]
                }
            ],
            "path": [
                {"title": "Пробный урок",
                 "text": "Знакомимся с ребёнком, определяем уровень и интересы, создаём первый проект.",
                 "accent": "#E769E4", "icon": "🎯"},
                {"title": "Основы",
                 "text": "Осваиваем базовые понятия: переменные, циклы, условия. Пишем первые программы.",
                 "accent": "#6E65FF", "icon": "📚"},
                {"title": "Практика",
                 "text": "Ребёнок делает собственные проекты: игры, боты, программы. Преподаватель рядом.",
                 "accent": "#1DE9B6", "icon": "💻"},
                {"title": "Продвинутый уровень",
                 "text": "Осваиваем серьёзные инструменты: Django, алгоритмы, олимпиадные задачи.", "accent": "#FFC75C",
                 "icon": "🏆"}
            ],
            "projects": [
                {"icon": "🎮", "title": "Игра на Scratch",
                 "text": "Платформер или аркада с персонажами, уровнями и подсчётом очков."},
                {"icon": "🤖", "title": "Telegram-бот",
                 "text": "Бот на Python, который отвечает на вопросы, отправляет картинки и помогает в учёбе."},
                {"icon": "🌐", "title": "Сайт на Django",
                 "text": "Полноценный сайт с регистрацией, базой данных и админкой."},
                {"icon": "👾", "title": "2D-игра на C++",
                 "text": "Классическая игра: змейка, тетрис или собственный аркадный проект."}
            ],
            "for_whom": [
                {"age": "6-9 лет", "title": "Младшим школьникам",
                 "text": "Подойдёт Scratch и «Компьютер с нуля» — знакомство с логикой через игры."},
                {"age": "10-13 лет", "title": "Средним школьникам",
                 "text": "Python и C++ — можно переходить от блоков к настоящему коду."},
                {"age": "14-17 лет", "title": "Старшим школьникам",
                 "text": "Олимпиады, серьёзные проекты, подготовка к будущей профессии."}
            ],
            "faq": [
                {"question": "С какого возраста можно начать?",
                 "answer": "С 6 лет — с курса «Компьютер с нуля» или Scratch. Дальше можно переходить к Python и другим языкам."},
                {"question": "Ребёнок никогда не программировал. Подойдёт?",
                 "answer": "Да, все курсы рассчитаны на старт с нуля. На пробном уроке преподаватель определит уровень и подберёт программу."},
                {"question": "Сколько длится курс?",
                 "answer": "От 6 месяцев до 2 лет в зависимости от курса и темпа ребёнка."},
                {"question": "Что нужно для занятий?",
                 "answer": "Компьютер, интернет и наушники. Преподаватель поможет настроить всё остальное."},
                {"question": "Можно ли попробовать бесплатно?",
                 "answer": "Да, первый урок — бесплатный. Ребёнок сразу сделает первый проект, а вы сможете задать вопросы."}
            ]
        }
        return render_page(request, "direction.html", csrf_protect, data)

    @app.get("/directions/games")
    async def direction_games(
            request: Request,
            csrf_protect: CsrfProtect = Depends()
    ):
        data = {
            "title": "Создание игр",
            "direction_name": "Создание игр",
            "accent": "#FFC75C",
            "hero_title": "Создание игр для детей 6–17 лет",
            "hero_subtitle": "Ребёнок делает свои игры — от идеи до готового проекта. Индивидуальные онлайн-занятия с преподавателем: Scratch, Roblox Studio и Unity.",
            "image": "/images/direction_games.webp",
            "image_position": "right",
            "learn": [
                {
                    "icon": "🎮",
                    "title": "Scratch — первые игры",
                    "accent": "#FFC75C",
                    "text": "Ребёнок собирает игры из блоков: персонажи, уровни, очки, события. Осваивает логику без сложного кода.",
                    "points": ["Логика и алгоритмы", "Игровая механика", "Анимация и события"]
                },
                {
                    "icon": "🕹️",
                    "title": "Roblox Studio — 3D-миры",
                    "accent": "#FF6E6E",
                    "text": "Создаёт собственные 3D-миры и игры в Roblox: строит локации, пишет скрипты на Lua.",
                    "points": ["3D-моделирование", "Скрипты Lua", "Игровой дизайн"]
                },
                {
                    "icon": "🎯",
                    "title": "Unity — серьёзные игры",
                    "accent": "#1DE9B6",
                    "text": "Разработка 2D и 3D игр на C#: от простых уровней до мультиплеера. Публикация своих проектов.",
                    "points": ["Язык C#", "2D-игры", "Мультиплеерные 3D-игры"]
                },
                {
                    "icon": "🎨",
                    "title": "Геймдизайн и графика",
                    "accent": "#E769E4",
                    "text": "Учится придумывать интересные механики и работать с графикой внутри игровых движков.",
                    "points": ["Игровая механика", "Баланс и уровни", "Визуальный стиль"]
                }
            ],
            "path": [
                {"title": "Пробный урок", "text": "Знакомимся, играем в первую игру, определяем интересы ребёнка.",
                 "accent": "#FFC75C", "icon": "🎯"},
                {"title": "Основы игр",
                 "text": "Осваиваем персонажей, уровни, события. Собираем первую игру на Scratch.", "accent": "#FF6E6E",
                 "icon": "🎮"},
                {"title": "Практика", "text": "Переходим к 3D-мирам: Roblox Studio или Unity. Делаем свои проекты.",
                 "accent": "#1DE9B6", "icon": "💻"},
                {"title": "Своя игра", "text": "Доводим проект до готовой игры: полировка, публикация, показ друзьям.",
                 "accent": "#E769E4", "icon": "🏆"}
            ],
            "projects": [
                {"icon": "🏃", "title": "Платформер на Scratch", "text": "Игра с уровнями, врагами и подсчётом очков."},
                {"icon": "🌍", "title": "3D-мир в Roblox", "text": "Своя локация с квестами и скриптами на Lua."},
                {"icon": "🚗", "title": "Гонки на Unity", "text": "2D или 3D гонка с физикой и управлением."},
                {"icon": "⚔️", "title": "Мультиплеерная игра", "text": "Игра на двоих с сетевым режимом на Unity."},
                {"icon": "🐍", "title": "Змейка на Python",
                 "text": "Классическая аркада — как первый шаг к программированию."},
                {"icon": "🎨", "title": "Дизайн уровней",
                 "text": "Собственная карта с продуманными локациями и ловушками."}
            ],
            "for_whom": [
                {"age": "6-9 лет", "title": "Младшим школьникам",
                 "text": "Scratch — первое знакомство с играми и логикой через блоки."},
                {"age": "10-13 лет", "title": "Средним школьникам",
                 "text": "Roblox Studio — можно создавать 3D-миры и писать скрипты."},
                {"age": "14-17 лет", "title": "Старшим школьникам",
                 "text": "Unity и C# — серьёзная разработка собственных игр."}
            ],
            "faq": [
                {"question": "С какого возраста можно начать?",
                 "answer": "С 6 лет — со Scratch. В 8-9 можно переходить на Roblox Studio, а с 12 — на Unity."},
                {"question": "Ребёнок любит играть, но не программировал. Подойдёт?",
                 "answer": "Да, все курсы рассчитаны на старт с нуля. Интерес к играм помогает — это становится основой обучения."},
                {"question": "Что нужно для занятий?",
                 "answer": "Компьютер, интернет и наушники. Программы устанавливаем вместе с преподавателем на пробном уроке."},
                {"question": "Ребёнок сможет опубликовать свою игру?",
                 "answer": "Да, в Roblox и Unity есть возможность публикации. Поможем пройти все шаги."},
                {"question": "Можно попробовать бесплатно?",
                 "answer": "Да, первый урок бесплатный. Ребёнок создаст свою первую игру уже на нём."}
            ]
        }
        return render_page(request, "direction.html", csrf_protect, data)

    @app.get("/directions/design")
    async def direction_design(
            request: Request,
            csrf_protect: CsrfProtect = Depends()
    ):
        data = {
            "title": "Дизайн и 3D",
            "direction_name": "Дизайн и 3D",
            "accent": "#E769E4",
            "hero_title": "Дизайн и 3D для детей 6–17 лет",
            "hero_subtitle": "Учим создавать красивые интерфейсы, графику и 3D-модели. Индивидуальные онлайн-занятия в Figma и Blender — от первых иллюстраций до собственного портфолио.",
            "image": "/images/direction_design.webp",
            "image_position": "center",
            "learn": [
                {
                    "icon": "🎨",
                    "title": "Figma — дизайн и графика",
                    "accent": "#E769E4",
                    "text": "Ребёнок учится рисовать иллюстрации, стикерпаки, дизайн сайтов и приложений.",
                    "points": ["Иллюстрации и стикерпаки", "Дизайн сайтов и приложений", "Анимация и портфолио"]
                },
                {
                    "icon": "🗿",
                    "title": "Blender — 3D-моделирование",
                    "accent": "#6E65FF",
                    "text": "Создаёт объёмные модели, персонажей и анимации — от простых объектов до сложных сцен.",
                    "points": ["3D-моделирование", "Текстуры и материалы", "Анимация"]
                },
                {
                    "icon": "🌈",
                    "title": "Цвет и композиция",
                    "accent": "#FFC75C",
                    "text": "Разбирается, как работают цвет, форма и композиция — это основа любого дизайна.",
                    "points": ["Работа с цветом", "Композиция", "Стиль и типографика"]
                },
                {
                    "icon": "💼",
                    "title": "Портфолио проектов",
                    "accent": "#1DE9B6",
                    "text": "Собирает собственное портфолио из проектов — реальных работ, которые можно показать.",
                    "points": ["Свои проекты", "Оформление портфолио", "Презентация работ"]
                }
            ],
            "path": [
                {"title": "Пробный урок", "text": "Знакомимся, пробуем рисовать в Figma или моделировать в Blender.",
                 "accent": "#E769E4", "icon": "🎯"},
                {"title": "Основы дизайна", "text": "Изучаем цвет, форму и композицию. Делаем первые работы.",
                 "accent": "#FFC75C", "icon": "🎨"},
                {"title": "Практика", "text": "Создаём иллюстрации, дизайн сайтов или 3D-модели. Собираем портфолио.",
                 "accent": "#6E65FF", "icon": "💻"},
                {"title": "Свой проект",
                 "text": "Работаем над собственным проектом — от идеи до финальной презентации.", "accent": "#1DE9B6",
                 "icon": "🏆"}
            ],
            "projects": [
                {"icon": "🌈", "title": "Иллюстрация в Figma",
                 "text": "Собственный рисунок с проработкой цвета и композиции."},
                {"icon": "📱", "title": "Дизайн приложения",
                 "text": "Макет мобильного приложения с экранами и иконками."},
                {"icon": "🌐", "title": "Дизайн сайта", "text": "Макет лендинга или интернет-магазина в Figma."},
                {"icon": "🧸", "title": "3D-персонаж", "text": "Объёмная модель персонажа в Blender."},
                {"icon": "🏠", "title": "3D-сцена", "text": "Окружение или интерьер с текстурами и освещением."},
                {"icon": "🎬", "title": "Анимация", "text": "Анимированный ролик с персонажем или 3D-объектом."}
            ],
            "for_whom": [
                {"age": "6-9 лет", "title": "Младшим школьникам",
                 "text": "Figma — простые иллюстрации и первые работы с цветом."},
                {"age": "10-13 лет", "title": "Средним школьникам",
                 "text": "Figma + Blender — можно делать дизайн и 3D-модели."},
                {"age": "14-17 лет", "title": "Старшим школьникам",
                 "text": "Серьёзные проекты, портфолио, подготовка к будущей профессии."}
            ],
            "faq": [
                {"question": "С какого возраста можно начать?",
                 "answer": "С 7 лет — с курса по Figma. С 10 лет можно добавить Blender."},
                {"question": "Нужен ли графический планшет?",
                 "answer": "Нет, для занятий достаточно компьютера и мышки. Планшет — по желанию."},
                {"question": "Ребёнок не умеет рисовать. Подойдёт?",
                 "answer": "Да, всему научим с нуля. Дизайн — это не только рисование, но и логика, композиция, работа с цветом."},
                {"question": "Что нужно для занятий?",
                 "answer": "Компьютер, интернет и наушники. Все программы работают в браузере или устанавливаются вместе с преподавателем."},
                {"question": "Можно попробовать бесплатно?",
                 "answer": "Да, первый урок бесплатный. Ребёнок сделает первую работу уже на нём."}
            ]
        }
        return render_page(request, "direction.html", csrf_protect, data)

    @app.get("/directions/web")
    async def direction_web(
            request: Request,
            csrf_protect: CsrfProtect = Depends()
    ):
        data = {
            "title": "Веб-разработка",
            "direction_name": "Веб-разработка",
            "accent": "#1DE9B6",
            "hero_title": "Веб-разработка для детей 6–17 лет",
            "hero_subtitle": "Учим создавать сайты с нуля — от макета до публикации в интернете. Индивидуальные онлайн-занятия: HTML, CSS, JavaScript, React и Django.",
            "image": "/images/direction_web.webp",
            "image_position": "right",
            "learn": [
                {
                    "icon": "🌐",
                    "title": "HTML и CSS — основа сайта",
                    "accent": "#1DE9B6",
                    "text": "Ребёнок учится верстать страницы: текст, картинки, кнопки, адаптивность под телефон.",
                    "points": ["Разметка страниц", "Стили и цвета", "Адаптивность"]
                },
                {
                    "icon": "⚡",
                    "title": "JavaScript — оживляем сайт",
                    "accent": "#FFC75C",
                    "text": "Добавляет интерактив: кнопки, анимации, формы, игры прямо в браузере.",
                    "points": ["Основы JS", "События и логика", "Мини-проекты"]
                },
                {
                    "icon": "⚛️",
                    "title": "React — современный подход",
                    "accent": "#6E65FF",
                    "text": "Осваивает популярный фреймворк, на котором делают большинство современных сайтов.",
                    "points": ["Компоненты", "Состояние", "Современный UI"]
                },
                {
                    "icon": "🚀",
                    "title": "Публикация сайта",
                    "accent": "#E769E4",
                    "text": "Учится публиковать свой проект в интернете — сайт смогут открыть друзья и родители.",
                    "points": ["Домен и хостинг", "Публикация", "Работа с Git"]
                }
            ],
            "path": [
                {"title": "Пробный урок", "text": "Знакомимся, создаём первую страницу прямо на уроке.",
                 "accent": "#1DE9B6", "icon": "🎯"},
                {"title": "Основы вёрстки",
                 "text": "Изучаем HTML и CSS. Делаем страницы с текстом, картинками и стилями.", "accent": "#FFC75C",
                 "icon": "🌐"},
                {"title": "Интерактив", "text": "Добавляем JavaScript и React. Сайт становится живым и современным.",
                 "accent": "#6E65FF", "icon": "💻"},
                {"title": "Публикация", "text": "Выкладываем сайт в интернет и показываем результат.",
                 "accent": "#E769E4", "icon": "🏆"}
            ],
            "projects": [
                {"icon": "📄", "title": "Личный сайт", "text": "Страница о себе с фотографиями и информацией."},
                {"icon": "🎮", "title": "Игра в браузере",
                 "text": "Простая аркада на JavaScript, работающая прямо в браузере."},
                {"icon": "🛒", "title": "Мини-магазин", "text": "Сайт с карточками товаров и корзиной."},
                {"icon": "📝", "title": "To-Do приложение",
                 "text": "Список задач с сохранением и удалением — на React."},
                {"icon": "🌍", "title": "Сайт на Django",
                 "text": "Полноценный сайт с базой данных и админкой на Python."},
                {"icon": "🎨", "title": "Портфолио-сайт", "text": "Красивая страница с собственными проектами."}
            ],
            "for_whom": [
                {"age": "9-12 лет", "title": "Средним школьникам",
                 "text": "HTML и CSS — простые сайты, потом JavaScript и React."},
                {"age": "13-15 лет", "title": "Подросткам",
                 "text": "Полноценная веб-разработка: React, Django, публикация."},
                {"age": "16-17 лет", "title": "Старшим школьникам",
                 "text": "Серьёзные проекты, портфолио, подготовка к профессии."}
            ],
            "faq": [
                {"question": "С какого возраста можно начать?",
                 "answer": "С 9 лет. Ребёнок должен уверенно пользоваться компьютером и клавиатурой."},
                {"question": "Ребёнок никогда не программировал. Подойдёт?",
                 "answer": "Да, курсы рассчитаны на старт с нуля. Начинаем с простой вёрстки и постепенно переходим к программированию."},
                {"question": "Нужно ли что-то устанавливать?",
                 "answer": "Нет, для вёрстки и JavaScript достаточно браузера. Для React и Django преподаватель поможет настроить всё."},
                {"question": "Ребёнок сможет показать свой сайт?",
                 "answer": "Да, мы учим публиковать проекты в интернете. Сайт смогут открыть друзья и родители по ссылке."},
                {"question": "Можно попробовать бесплатно?",
                 "answer": "Да, первый урок бесплатный. Ребёнок создаст свою первую страницу уже на нём."}
            ]
        }
        return render_page(request, "direction.html", csrf_protect, data)

    @app.get("/offer")
    async def offer_page(request: Request, csrf_protect: CsrfProtect = Depends()):
        return render_page(request, "offer.html", csrf_protect)

    @app.get("/privacy")
    async def privacy_policy(request: Request, csrf_protect: CsrfProtect = Depends()):
        return render_page(request, "privacy.html", csrf_protect)

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
