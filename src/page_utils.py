from pathlib import Path

from fastapi.templating import Jinja2Templates

ROOT_DIRECTORY = Path(__file__).resolve().parent.parent
TEMPLATES_DIRECTORY = ROOT_DIRECTORY / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIRECTORY))


def render_page(request, template_name, csrf_protect, context=None):
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()

    template_context = {
        "request": request,
        "csrf_token": csrf_token,
        **(context or {})
    }

    response = templates.TemplateResponse(template_name, template_context)
    csrf_protect.set_csrf_cookie(signed_token, response)

    return response
