from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import or_, select
from database import get_db
from routers.auth import get_current_employee
from models import Employees, Tasks, ProjectMemberRoles
from datetime import date
from routers.auth import ADMIN_ROLE_ID, PM_ROLE_ID

router = APIRouter(prefix='/projects/{project_id}/tasks', tags=['tasks'])

@router.get('', status_code=status.HTTP_200_OK)
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

@router.post('', status_code=status.HTTP_201_CREATED)
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

class TaskUpdateRequest(BaseModel):
  id: int
  title: str | None = Field(default=None, min_length=1, max_length=255)
  description: str | None = Field(default=None)
  status: str | None = Field(default=None, min_length=1, max_length=100)
  start_date: date | None = Field(default=None)
  end_date: date | None = Field(default=None)
  pull_request: str | None = Field(default=None)

@router.patch('/edittask', status_code=status.HTTP_200_OK)
def edit_task_info(
  project_id: int,
  data: TaskUpdateRequest,
  session: Session = Depends(get_db),
  employee: Employees = Depends(get_current_employee)
):
  task = session.get(Tasks, data.id)
  if not task:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='Task not found'
    )

  is_editor = session.scalar(
    select(ProjectMemberRoles)
    .where(
      ProjectMemberRoles.project_id == project_id,
      ProjectMemberRoles.employee_id == employee.id,
      or_(
        ProjectMemberRoles.role_id == ADMIN_ROLE_ID,
        ProjectMemberRoles.role_id == PM_ROLE_ID
      )
    )
  )
  if not is_editor:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail='You dont have permission to edit current task'
    )

  update_dict = data.model_dump(exclude_unset=True)
  update_dict.pop('id', None)

  if update_dict:
    try:
      for key, value in update_dict.items():
        setattr(task, key, value)
      session.commit()
      session.refresh(task)
    except Exception as error:
      session.rollback()
      raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f'Failed task info update: {error}'
      )

  return task