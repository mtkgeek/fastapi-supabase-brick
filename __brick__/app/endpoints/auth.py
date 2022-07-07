

import json
from urllib import response
from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.responses import JSONResponse


from app.config import Settings, get_settings

from app.models import auth_models
from app.database.database import supabase_client
from app.dependencies import authorization_dep

router = APIRouter()


settings: Settings = get_settings()


def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None


@router.post("/sign-up", status_code=status.HTTP_200_OK)
async def sign_up(body: auth_models.SignUpModel):
    try:
        response_obj = supabase_client.auth.sign_up(
            email=body.email, password=body.password)

        # pp_json(response_obj.json())

        session_obj = auth_models.SessionModel.parse_obj(
            json.loads(response_obj.json()))

        print(session_obj.user)

        if not session_obj.user:
            raise HTTPException(
                status_code=401, detail="Couldn't create user")

        # check if user already exists. Supabase doesn't raise an error if
        # the same email is used for registering twice

        user_data = supabase_client.table("users").select(
            "*").eq("id", session_obj.user.id).execute()

        if len(user_data.data) > 0:

            raise HTTPException(
                status_code=401, detail="User with this email already exists")

        data = supabase_client.table("users").insert(
            {"email": body.email, "name": body.name, "id": session_obj.user.id, "token": session_obj.access_token, "refresh_token": session_obj.refresh_token}).execute()
        # print(data)
        if not data:
            raise HTTPException(
                status_code=401, detail="Couldn't create user")

        # user = json.dumps({**json.loads(session_obj.user.json()), **
        #                    {"access_token": session_obj.access_token, "refresh_token": session_obj.refresh_token}})

        return JSONResponse(content={"data": data.data}, status_code=200, media_type="application/json")

    except Exception as ex:
        print("Exception", ex)
        raise HTTPException(
            status_code=401, detail="Couldn't create user")


@router.post("/log-in", status_code=status.HTTP_200_OK)
async def log_in(body: auth_models.LoginModel):
    try:
        response_obj = supabase_client.auth.sign_in(
            email=body.email, password=body.password)

        session_obj = auth_models.SessionModel.parse_obj(
            json.loads(response_obj.json()))

        if not session_obj.user:
            raise HTTPException(
                status_code=400, detail="Couldn't log in, wrong email/password")

        user_data = supabase_client.table("users").select(
            "*").eq("id", session_obj.user.id).execute()

        if len(user_data.data) < 1:

            raise HTTPException(
                status_code=401, detail="User with this email not found")

        print(user_data)
        print(user_data.data)

        user = user_data.data

        # user = json.dumps({**json.loads(session_obj.user.json()), **
        #                    {"access_token": session_obj.access_token, "refresh_token": session_obj.refresh_token}})

        return JSONResponse(content={"data": user}, status_code=200, media_type="application/json")

    except Exception as ex:
        print("Exception", ex)
        raise HTTPException(
            status_code=400, detail="Couldn't log in, wrong email/password")


@router.get("/get-user", status_code=status.HTTP_200_OK)
async def get_user(user: auth_models.User = Depends(authorization_dep.has_access)):

    user_data = supabase_client.table("users").select(
        "*").eq("id", user.id).execute()

    if len(user_data.data) < 1:

        raise HTTPException(
            status_code=401, detail="User with this email not found")

    print(user_data)
    print(user_data.data)

    user = user_data.data
    return JSONResponse(content={"user": user}, status_code=200, media_type="application/json")


@router.post("/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_token(body: auth_models.RefreshTokenModel):
    try:
        new_session = supabase_client.auth.api.refresh_access_token(
            refresh_token=body.refresh_token)
        # print(new_access_token_session)
        session_obj = auth_models.SessionModel.parse_obj(
            json.loads(new_session.json()))
        if not session_obj.access_token:
            raise HTTPException(
                status_code=401, detail="Couldn't refresh access token")
        return JSONResponse(content={"access_token": session_obj.access_token}, status_code=200, media_type="application/json")

    except Exception as ex:
        print("Exception", ex)
        raise HTTPException(
            status_code=401, detail="Couldn't refresh access token")


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(body: auth_models.ResetPasswordModel):
    try:
        data = supabase_client.auth.api.reset_password_for_email(
            email=body.email)
        if data is None:
            return JSONResponse(content={"status": "Password reset email sent successfully"}, status_code=200, media_type="application/json")
        raise HTTPException(
            status_code=401, detail="Couldn't send reset email")

    except Exception as ex:
        print("Exception", ex)
        raise HTTPException(
            status_code=401, detail="Couldn't send reset email")

