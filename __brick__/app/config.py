import logging
import os
from functools import lru_cache

from pydantic import BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    # use_ngrok: str = os.getenv(
    #     "USE_NGROK", True)
    # firebase_admin_key: str = os.getenv(
    #     "FIREBASE_ADMIN_KEY", "firebase-a.json")
    supabase_url: str = os.getenv(
        "SUPABASE_URL", "testnetrh5lAFGlMX8bYTwXsVbbdv3s5IKMrmUb")

    supabase_key: str = os.getenv(
        "SUPABASE_KEY", "testnetrh5lAFGlMX8bYTwXsVbbdv3s5IKMrmUb")

    mail_username: str = os.getenv(
        "MAIL_USERNAME", "dsfcghvj")
    mail_password: str = os.getenv(
        "MAIL_PASSWORD", "dxfgc")
    mail_to: str = os.getenv("MAIL_TO", "support@blank.com")
    mail_from: str = os.getenv("MAIL_FROM", "blank@mail.com")
    mail_port: int = os.getenv("MAIL_PORT", 45)
    mail_server: str = os.getenv("MAIL_SERVER", "bghj")


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
