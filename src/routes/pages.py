from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse
from fastapi_csrf_protect import CsrfProtect

from src.courses_data import COURSES, POPULAR_COURSES
from src.directions_data import DIRECTIONS
from src.page_utils import ROOT_DIRECTORY, render_page

router = APIRouter()


@router.get("/")
async def index(request: Request, csrf_protect: CsrfProtect = Depends()):
    return render_page(
        request,
        "index.html",
        csrf_protect,
        {"popular_courses": POPULAR_COURSES}
    )


@router.get("/thank-you")
async def thank_you(request: Request, csrf_protect: CsrfProtect = Depends()):
    return render_page(request, "thank_you.html", csrf_protect)


@router.get("/courses")
async def courses_page(request: Request, csrf_protect: CsrfProtect = Depends()):
    return render_page(
        request,
        "courses.html",
        csrf_protect,
        {"courses": COURSES}
    )


@router.get("/directions/programming")
async def direction_programming(request: Request, csrf_protect: CsrfProtect = Depends()):
    return render_page(request, "direction.html", csrf_protect, DIRECTIONS["programming"])


@router.get("/directions/games")
async def direction_games(request: Request, csrf_protect: CsrfProtect = Depends()):
    return render_page(request, "direction.html", csrf_protect, DIRECTIONS["games"])


@router.get("/directions/design")
async def direction_design(request: Request, csrf_protect: CsrfProtect = Depends()):
    return render_page(request, "direction.html", csrf_protect, DIRECTIONS["design"])


@router.get("/directions/web")
async def direction_web(request: Request, csrf_protect: CsrfProtect = Depends()):
    return render_page(request, "direction.html", csrf_protect, DIRECTIONS["web"])


@router.get("/offer")
async def offer_page(request: Request, csrf_protect: CsrfProtect = Depends()):
    return render_page(request, "offer.html", csrf_protect)


@router.get("/privacy")
async def privacy_policy(request: Request, csrf_protect: CsrfProtect = Depends()):
    return render_page(request, "privacy.html", csrf_protect)


@router.get("/sitemap.xml")
async def sitemap():
    path = ROOT_DIRECTORY / "static" / "sitemap.xml"
    return FileResponse(str(path), media_type="application/xml")


@router.get("/courses.xml", include_in_schema=False)
async def courses_feed():
    path = ROOT_DIRECTORY / "static" / "courses.xml"
    return FileResponse(str(path), media_type="application/xml")


@router.get("/robots.txt")
async def robots():
    path = ROOT_DIRECTORY / "static" / "robots.txt"
    return FileResponse(str(path), media_type="text/plain")


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    path = ROOT_DIRECTORY / "static" / "icons" / "favicon.ico"
    return FileResponse(path)


@router.get("/apple-touch-icon.png", include_in_schema=False)
async def apple_touch_icon():
    path = ROOT_DIRECTORY / "static" / "icons" / "apple-touch-icon.png"
    return FileResponse(path)


@router.get("/favicon-16x16.png", include_in_schema=False)
async def favicon_16():
    path = ROOT_DIRECTORY / "static" / "icons" / "favicon-16x16.png"
    return FileResponse(path)


@router.get("/favicon-32x32.png", include_in_schema=False)
async def favicon_32():
    path = ROOT_DIRECTORY / "static" / "icons" / "favicon-32x32.png"
    return FileResponse(path)


@router.get("/android-chrome-192x192.png", include_in_schema=False)
async def android_192():
    path = ROOT_DIRECTORY / "static" / "icons" / "android-chrome-192x192.png"
    return FileResponse(path)


@router.get("/android-chrome-512x512.png", include_in_schema=False)
async def android_512():
    path = ROOT_DIRECTORY / "static" / "icons" / "android-chrome-512x512.png"
    return FileResponse(path)
