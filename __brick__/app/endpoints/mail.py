from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import json

from starlette.responses import JSONResponse
from app.config import Settings, get_settings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.models.mail_models import MailModel


# init firebase
settings: Settings = get_settings()


router = APIRouter()


async def simple_send(email: MailModel) -> JSONResponse:

    html = f"""
            <p>{email.body}</p>
            <br/>
            <p>From: {email.from_mail}</p> 
        """

    message = MessageSchema(

        subject=email.subject,
        # List of recipients, as many as you can pass
        recipients=email.receipients,

        html=html,
        subtype="html"
    )

    conf = ConnectionConfig(
        MAIL_USERNAME=settings.mail_username,
        MAIL_PASSWORD=settings.mail_password,
        MAIL_FROM=settings.mail_from,
        MAIL_FROM_NAME=email.from_name,
        MAIL_PORT=settings.mail_port,
        MAIL_SERVER=settings.mail_server,
        MAIL_TLS=True,
        MAIL_SSL=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@router.post("/send-email", status_code=200)
async def send_notification(email: MailModel, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        simple_send, email)
    return {"message": "email sent in the background"}
