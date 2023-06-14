from fastapi.staticfiles import StaticFiles
from app.router import public, pay, api


def init_router(app):
    app.mount("/static", StaticFiles(directory="./static"), name="static")
    app.include_router(public.router)
    app.include_router(pay.router)
    app.include_router(api.router)
