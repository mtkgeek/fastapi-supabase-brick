# import os

import arel

import os

from watchfiles import watch


from fastapi.logger import logger
import sys

import logging
from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Depends

from app.config import Settings, get_settings
from app.dependencies.authorization_dep import has_access
from app.endpoints import auth
from app.website import auth_site, web_config


from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


log = logging.getLogger("uvicorn")


settings: Settings = get_settings()

# print("fuuuuckkk")
# print(settings.debug)
# print(os.getenv("DEBUG"))


# routes
PROTECTED = Depends(has_access)


origins = [

    # "http://0.0.0.0:5000",
    "*",
]


def create_application() -> FastAPI:
    application = FastAPI()
    application.mount(
        "/static", StaticFiles(directory="static"), name="static")

    if _debug := os.getenv("DEBUG"):
        hot_reload = arel.HotReload(paths=[arel.Path("./templates")])
        application.add_websocket_route(
            "/hot-reload", route=hot_reload, name="hot-reload")
        application.add_event_handler("startup", hot_reload.startup)
        application.add_event_handler("shutdown", hot_reload.shutdown)
        web_config.templates.env.globals["DEBUG"] = _debug
        web_config.templates.env.globals["hot_reload"] = hot_reload

    application.include_router(auth_site.router, tags=["auth-site"])
    application.include_router(auth.router, tags=["auth"])
    # application.include_router(
    #     push_notifications.router, tags=["push-notification"], , prefix="/hello",
    # dependencies = [PROTECTED])
    # application.include_router(
    #     mail.router, tags=["mail"])

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],

    )

    return application


app = create_application()


# app.mount("/static", StaticFiles(directory="./static"), name="static")

# uvicorn --host 127.0.0.1 --port 8000 --workers 4 app.main:create_application --reload --factory
