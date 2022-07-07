from fastapi.logger import logger
import sys

import logging
from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Depends

from app.config import Settings, get_settings
from app.dependencies.authorization_dep import has_access
from app.endpoints import auth


log = logging.getLogger("uvicorn")
settings: Settings = get_settings()

# routes
PROTECTED = Depends(has_access)


origins = [

    # "http://0.0.0.0:5000",
    "*",
]


def create_application() -> FastAPI:
    application = FastAPI()

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
# uvicorn --host 127.0.0.1 --port 8000 --workers 4 app.main:create_application --reload --factory
