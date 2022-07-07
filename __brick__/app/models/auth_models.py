from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SignUpModel(BaseModel):
    email: str
    password: str
    name: str


class LoginModel(BaseModel):
    email: str
    password: str


class RefreshTokenModel(BaseModel):
    refresh_token: str


class ResetPasswordModel(BaseModel):
    email: str

# supabase session and user related


class AppMetadata(BaseModel):
    provider: str
    providers: List[str]


class IdentityData(BaseModel):
    sub: str


class Identity(BaseModel):
    id: str
    user_id: str
    provider: str
    created_at: str
    updated_at: str
    identity_data: IdentityData
    last_sign_in_at: str


class User(BaseModel):
    app_metadata: AppMetadata
    aud: str
    created_at: str
    id: str
    user_metadata: Dict[str, Any]
    identities: List[Identity]
    confirmation_sent_at: Any
    action_link: Any
    last_sign_in_at: str
    phone: str
    phone_confirmed_at: Any
    recovery_sent_at: Any
    role: str
    updated_at: str
    email_confirmed_at: str
    confirmed_at: Any
    invited_at: Any
    email: str
    new_email: Any
    email_change_sent_at: Any
    new_phone: Any
    phone_change_sent_at: Any


class SessionModel(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_at: Optional[int] = None
    expires_in: Optional[int] = None
    provider_token: Optional[Any] = None
    refresh_token: Optional[str] = None
    user: Optional[User] = None
