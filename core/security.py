from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from core.config import settings
from core.logger_config import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    logger.info(f"Creating access token for user: {data.get('sub', 'unknown')}")
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire, "refresh": True})
    logger.info(f"Creating refresh token for user: {data.get('sub', 'unknown')}")
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if not payload.get("refresh"):
            logger.warning("Invalid refresh token: missing refresh flag")
            return None
        logger.info(f"Successfully verified refresh token for user: {payload.get('sub', 'unknown')}")
        return payload
    except jwt.JWTError:
        logger.error("Failed to verify refresh token")
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    result = pwd_context.verify(plain_password, hashed_password)
    if not result:
        logger.warning("Password verification failed")
    return result


def get_password_hash(password: str) -> str:
    logger.debug("Generating password hash")
    return pwd_context.hash(password)
