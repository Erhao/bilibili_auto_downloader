import jwt
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, Header
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
#
from app.model.user import User
# from ..db.mongodb import AsyncIOMotorClient, get_database
# from ..models.token import TokenPayload
# from ..models.user import User

from .config import JWT_TOKEN_PREFIX, SECRET_KEY


ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def _get_authorization_token(authorization: str = Header(...)):
    token_prefix, token = authorization.split(" ")
    if token_prefix != JWT_TOKEN_PREFIX:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid authorization type"
        )

    return token


def _parse_token(
    token: str = Depends(_get_authorization_token)
):
    try:
        token_data = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    return token_data


async def get_current_user(
    token_data: dict = Depends(_parse_token)
) -> User:
    uid = token_data.get('uid')
    user = await User.get_from_oid(uid)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    return user

#
#
# def _get_authorization_token_optional(authorization: str = Header(None)):
#     if authorization:
#         return _get_authorization_token(authorization)
#     return ""
#
#
# async def _get_current_user_optional(
#     db: AsyncIOMotorClient = Depends(get_database),
#     token: str = Depends(_get_authorization_token_optional),
# ) -> Optional[User]:
#     if token:
#         return await _get_current_user(db,  token)
#
#     return None
#
#
# def get_current_user_authorizer(*, required: bool = True):
#     if required:
#         return _get_current_user
#     else:
#         return _get_current_user_optional


def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    # if expires_delta:
    #     expire = datetime.utcnow() + expires_delta
    # else:
    #     expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt
