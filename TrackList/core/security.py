import jwt
from datetime import datetime, timedelta, timezone
from core.config import settings

def create_jwt_token(employee_id: int):
  expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_TOKEN_EXPIRE_HOURS)

  payload = {
    "sub": str(employee_id),
    "exp": expire
  }

  return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_jwt_token(token: str):
  payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
  return payload