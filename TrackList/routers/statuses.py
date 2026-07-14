from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import or_, select
from database import get_db
from routers.auth import get_current_employee
from models import Employees, Statuses, ProjectMemberRoles, Tasks
from routers.auth import ADMIN_ROLE_ID, PM_ROLE_ID

router = APIRouter(prefix='/projects/{project_id}/statuses', tags=['statuses'])

@router.get('', status_code=status.HTTP_200_OK)
def read_all_statuses(
  project_id: int,
  session: Session = Depends(get_db)
):
  statement = (select(Statuses).where(Statuses.project_id == project_id))
  project_statuses = session.scalars(statement).all()
  return project_statuses

class StatusRequest(BaseModel):
  title: str = Field(min_length=1, max_length=50)

@router.post('', status_code=status.HTTP_201_CREATED)
def create_project_status(
  project_id: int,
  data: StatusRequest,
  session: Session = Depends(get_db),
  employee: Employees = Depends(get_current_employee)
):
  has_permission = session.scalar(
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
  if not has_permission:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail='You dont have permission to create project statuses'
    )

  try:
    new_status = Statuses(**data.model_dump(), project_id=project_id)
    session.add(new_status)
    session.commit()
    session.refresh(new_status)
    return new_status

  except Exception as error:
    session.rollback()
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f'Failed to create the status: {error}'
    )

@router.delete('/{status_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_project_status(
  project_id: int,
  status_id: int,
  session: Session = Depends(get_db),
  employee: Employees = Depends(get_current_employee)
):
  has_permission = session.scalar(
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
  if not has_permission:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail='You dont have permission to delete project statuses'
    )

  status_item = session.get(Statuses, status_id)
  if not status_item:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='Status not found'
    )

  tasks_connected = session.scalar(
    select(Tasks).where(Tasks.status == status_item.title).limit(1)
  )
  if tasks_connected:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail='Cannot delete the status, because existed tasks contain it'
    )

  session.delete(status_item)
  session.commit()
  return