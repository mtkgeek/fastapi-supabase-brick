from typing import List
from pydantic import BaseModel


class MailModel(BaseModel):
    from_mail: str
    receipients: list
    from_name: str
    body: str
    subject: str
