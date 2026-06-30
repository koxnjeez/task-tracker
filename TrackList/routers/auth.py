from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from core.google_auth import verify_google_token
from core.security import create_jwt_token, decode_jwt_token
from database import get_db
from models import Employees
from starlette import status

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

def authenticate_with_google(session: Session, token: str):
  payload = verify_google_token(token)
  google_id = payload["sub"]

  employee = session.scalar(
    select(Employees).where(Employees.google_id == google_id)
  )

  if not employee:
    employee = Employees(
      google_id=payload["sub"],
      email=payload["email"],
      email_verified=payload.get("email_verified", False),

      first_name=payload.get("given_name"),
      last_name=payload.get("family_name"),
      middle_name=None,

      avatar_url=payload.get("picture"),
      phone_number=None
    )
    session.add(employee)
  else:
    employee.first_name = payload.get("given_name")
    employee.last_name = payload.get("family_name")
    employee.avatar_url = payload.get("picture")
    employee.email_verified = payload.get("email_verified", False)

  session.commit()
  session.refresh(employee)

  jwt_token = create_jwt_token(employee.id)
  return jwt_token, employee

class GoogleAuthRequest(BaseModel):
  token: str

@router.post("/google", status_code=status.HTTP_200_OK)
def google_login(request: GoogleAuthRequest, session: Session = Depends(get_db)):
  token, employee = authenticate_with_google(session, request.token)
  return {
    "access_token": token,
    "token_type": "bearer"
  }

def get_current_employee(
  credentials: HTTPAuthorizationCredentials = Depends(security),
  session: Session = Depends(get_db)
):
  token = credentials.credentials

  try:
    payload = decode_jwt_token(token)
  except Exception:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid token"
    )

  employee_id = int(payload.get("sub"))
  if not employee_id:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid payload"
    )

  employee = session.get(Employees, employee_id)
  if not employee:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Employee not found"
    )

  return employee

class EmployeeResponse(BaseModel):
  id: int
  email: str
  first_name: str | None
  last_name: str | None
  middle_name: str | None
  phone_number: str | None
  avatar_url: str | None

@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeResponse
)
def get_me(employee: Employees = Depends(get_current_employee)):
  return employee

class ProfileUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    middle_name: str = None
    phone_number: str = None

@router.patch('/updateinfo', status_code=status.HTTP_200_OK)
async def update_personal_info(
    data: ProfileUpdate,
    session: Session = Depends(get_db),
    employee: Employees = Depends(get_current_employee)
):
  update_dict = data.model_dump(exclude_unset=True)

  if update_dict:
    statement = (
        update(Employees)
        .where(Employees.id == employee.id)
        .values(update_dict)
    )
    session.execute(statement)

    session.commit()
    session.refresh(employee)

  return employee