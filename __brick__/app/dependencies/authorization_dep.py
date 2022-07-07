import json
from jose import jwt
from jose.exceptions import JOSEError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from app.database.database import supabase_client
from app.models import auth_models

security = HTTPBearer()


async def has_access(credentials: HTTPBasicCredentials = Depends(security)):
    """
        Function that is used to validate the token in the case that it requires it
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, key='secret', options={"verify_signature": False,
                                                           "verify_aud": False,
                                                           "verify_iss": False})

        if payload["aud"] != "authenticated":
            raise HTTPException(
                status_code=401, detail="Your token has probably expired")

        user = supabase_client.auth.api.get_user(jwt=token)

        if not user:
            raise HTTPException(
                status_code=401, detail="Your token has probably expired")
        else:

            return auth_models.User.parse_obj(
                json.loads(user.json()))
    except JOSEError as e:  # catches any exception
        raise HTTPException(
            status_code=401,
            detail=str(e))
