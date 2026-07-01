from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import insert, or_, select
from routers.auth import get_current_employee
from starlette import status
from sqlalchemy.orm import Session
from database import get_db
from models import Employees, Projects, ProjectMemberRoles

router = APIRouter(prefix="/projects", tags=["projects"])
ADMIN_ROLE_ID = 0

@router.get('/', status_code=status.HTTP_200_OK)
async def read_all_projects(
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

@router.post('/new-project', status_code=status.HTTP_201_CREATED)
async def create_project(
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