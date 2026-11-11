from fastapi.templating import Jinja2Templates

from . import config
from .activities import ACTIVITIES, ORDER, PLANS
from .config import BASE_DIR

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
templates.env.globals.update(cfg=config, ACTIVITIES=ACTIVITIES, ORDER=ORDER, PLANS=PLANS)
# Said next to every "follows the national curriculum" (app/bank/excluded.py is what leaves them out)
templates.env.globals["LEFT_OUT"] = ("Evolution, puberty and human reproduction are left out on purpose, so families can "
                                     "cover them their own way.")


def page(request, name: str, ctx=None, status_code: int = 200, **kw):
    return templates.TemplateResponse(request, name, {"ctx": ctx, **kw}, status_code=status_code)
