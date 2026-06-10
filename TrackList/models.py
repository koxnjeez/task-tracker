from database import Base
from sqlalchemy import BigInteger, Column, Date, Integer, SmallInteger, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Projects(Base):
  __tablename__ = 'projects'

  id = Column(BigInteger, primary_key=True, index=True)
  title = Column(String)

class Tasks(Base):
  __tablename__ = 'tasks'

  id = Column(BigInteger, primary_key=True, index=True)
  title = Column(String)
  description = Column(String)
  status = Column(String)
  start_date = Column(Date)
  end_date = Column(Date)
  pull_request = Column(String)
  project_id = Column(BigInteger, ForeignKey('projects.id'))

class Employees(Base):
  __tablename__ = 'employees'

  id = Column(BigInteger, primary_key=True, index=True)
  first_name = Column(String)
  last_name = Column(String)
  middle_name = Column(String)
  position = Column(String)
  email = Column(String)
  phone_number = Column(String)

class Roles(Base):
  __tablename__ = 'roles'

  id = Column(SmallInteger, primary_key=True, index=True)
  name = Column(String)

class ProjectMemberRoles(Base):
  __tablename__ = 'project_member_roles'

  id = Column(BigInteger, primary_key=True, index=True)
  project_id = Column(BigInteger, ForeignKey('projects.id'))
  employee_id = Column(BigInteger, ForeignKey('employees.id'))
  role_id = Column(SmallInteger, ForeignKey('roles.id'))

class Assignees(Base):
  __tablename__ = 'assignees'

  id = Column(BigInteger, primary_key=True, index=True)
  task_id = Column(BigInteger, ForeignKey('tasks.id'))
  employee_id = Column(BigInteger, ForeignKey('employees.id'))

class Tags(Base):
  __tablename__ = 'tags'

  id = Column(BigInteger, primary_key=True, index=True)
  title = Column(String)
  task_id = Column(BigInteger, ForeignKey('tasks.id'))

class Comments(Base):
  __tablename__ = 'comments'

  id = Column(BigInteger, primary_key=True, index=True)
  text = Column(String)
  employee_id = Column(BigInteger, ForeignKey('employees.id'))
  task_id = Column(BigInteger, ForeignKey('tasks.id'))
  time: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False
  )
  
class BacklogTasks(Base):
  __tablename__ = 'backlog_tasks'

  id = Column(BigInteger, primary_key=True, index=True)
  title = Column(String)
  description = Column(String)
  project_id = Column(BigInteger, ForeignKey('projects.id'))

class Statuses(Base):
  __tablename__ = 'statuses'

  id = Column(BigInteger, primary_key=True, index=True)
  title = Column(String)
  project_id = Column(BigInteger, ForeignKey('projects.id'))