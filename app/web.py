from fastapi.templating import Jinja2Templates

from . import config
from .activities import ACTIVITIES, ORDER, PLANS
from .config import BASE_DIR

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
templates.env.globals.update(cfg=config, ACTIVITIES=ACTIVITIES, ORDER=ORDER, PLANS=PLANS)


def page(request, name: str, ctx=None, status_code: int = 200, **kw):
    return templates.TemplateResponse(request, name, {"ctx": ctx, **kw}, status_code=status_code)
