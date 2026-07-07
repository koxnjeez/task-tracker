from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from routers.auth import get_current_employee
from models import Employees, Tasks
from datetime import date

router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.get('/', status_code=status.HTTP_200_OK)
def read_all_tasks(
  project_id: int,
  session: Session = Depends(get_db)
):
  statement = (select(Tasks).where(Tasks.project_id == project_id))
  project_tasks = session.scalars(statement).all()
  return project_tasks

class TaskRequest(BaseModel):
  title: str = Field(min_length=1, max_length=255)
  description: str | None = Field(default=None)
  status: str = Field(min_length=1, max_length=100)
  start_date: date | None = Field(default=None)
  end_date: date | None = Field(default=None)
  pull_request: str | None = Field(default=None)
  project_id: int

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_task(
  project_id: int,
  data: TaskRequest,
  session: Session = Depends(get_db)
):
  try:
    new_task = Tasks(**data.model_dump(), project_id=project_id)
    session.add(new_task)
    session.commit()
    return new_task
  except Exception as error:
    session.rollback()
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f'Failed to create the task: {error}'
    )