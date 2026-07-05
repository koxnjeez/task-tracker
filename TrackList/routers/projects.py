from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import or_, select
from routers.auth import get_current_employee
from starlette import status
from sqlalchemy.orm import Session
from database import get_db
from models import Employees, Projects, ProjectMemberRoles, Roles

router = APIRouter(prefix="/projects", tags=["projects"])
ADMIN_ROLE_ID = 1

@router.get('/', status_code=status.HTTP_200_OK)
def read_all_projects(
  session: Session = Depends(get_db),
  employee: Employees = Depends(get_current_employee)
):
  statement = (
    select(Projects)
    .join(ProjectMemberRoles, ProjectMemberRoles.project_id == Projects.id, isouter=True)
    .where(
      or_(
        Projects.is_private == False,
        ProjectMemberRoles.employee_id == employee.id
      )
    )
    .distinct()
  )

  employee_projects = session.scalars(statement).all()
  return employee_projects

class ProjectRequest(BaseModel):
  title: str = Field(min_length=1, max_length=255)
  is_private: bool = False

@router.post('/newproject', status_code=status.HTTP_201_CREATED)
def create_project(
  data: ProjectRequest,
  session: Session = Depends(get_db),
  employee: Employees = Depends(get_current_employee)
):
  try:
    new_project = Projects(
      title=data.title,
      is_private=data.is_private
    )
    session.add(new_project)
    session.flush() # для генерации id проекта, прокидываем запись но не коммитим

    new_project_member_role = ProjectMemberRoles(
      project_id=new_project.id,
      employee_id=employee.id,
      role_id=ADMIN_ROLE_ID
    )
    session.add(new_project_member_role)
    session.commit()

    session.refresh(new_project)
    return new_project
  except Exception as error:
    session.rollback()
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f'Failed to create the project: {error}'
    )

class ProjectUpdateRequest(BaseModel):
  id: int
  title: Optional[str] = Field(default=None, min_length=1, max_length=255)
  is_private: Optional[bool] = None

@router.patch('/editproject', status_code=status.HTTP_200_OK)
def edit_project_info(
  data: ProjectUpdateRequest,
  session: Session = Depends(get_db),
  employee: Employees = Depends(get_current_employee)
):
  project = session.get(Projects, data.id)
  if not project:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='Project not found'
    )

  is_admin = session.scalar(
    select(ProjectMemberRoles)
    .where(
      ProjectMemberRoles.project_id == data.id,
      ProjectMemberRoles.employee_id == employee.id,
      ProjectMemberRoles.role_id == ADMIN_ROLE_ID
    )
  )
  if not is_admin:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail='You dont have permission to edit current project'
    )

  update_dict = data.model_dump(exclude_unset=True)
  update_dict.pop('id', None)

  if update_dict:
    try:
      for key, value in update_dict.items():
        setattr(project, key, value) # в отличии от прямого запроса, работа с живым объектом и потом уже идет синхронизация с бд
      session.commit()
      session.refresh(project)
    except Exception as error:
      session.rollback()
      raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f'Failed project info update: {error}'
      )

  return project

@router.get('/roles', status_code=status.HTTP_200_OK)
def get_all_roles(
  session: Session = Depends(get_db)
):
  statement = (
    select(Roles)
    .order_by(Roles.id.asc())
  )

  all_roles = session.scalars(statement).all()
  return all_roles