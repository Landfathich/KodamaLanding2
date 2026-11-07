import logging

import uvicorn
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic_settings import BaseSettings

from src.page_utils import ROOT_DIRECTORY
from src.routes import pages, applications

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class CsrfSettings(BaseSettings):
    secret_key: str
    csrf_token_location: str = "header"
    cookie_samesite: str = "lax"
    cookie_secure: bool = True

    class Config:
        env_prefix = "CSRF_"


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


def make_up():
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )

    @app.exception_handler(CsrfProtectError)
    def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

    static_path = ROOT_DIRECTORY / "static"
    app.mount("/app/static", StaticFiles(directory=str(static_path)), name="static")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(pages.router)
    app.include_router(applications.router)

    return app


app = make_up()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5050, reload=True)
