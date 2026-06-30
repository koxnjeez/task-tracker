from database import Base
from sqlalchemy import BigInteger, Boolean, Column, Date, SmallInteger, String, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Projects(Base):
  __tablename__ = 'projects'

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String(255))

class Tasks(Base):
  __tablename__ = 'tasks'

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String(255))
  description: Mapped[str] = mapped_column(Text)
  status: Mapped[str] = mapped_column(String(100))
  start_date: Mapped[Date] = mapped_column(Date)
  end_date: Mapped[Date] = mapped_column(Date)
  pull_request: Mapped[str] = mapped_column(Text)
  project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('projects.id'))

class Employees(Base):
  __tablename__ = 'employees'

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  first_name: Mapped[str | None] = mapped_column(String(50))
  last_name: Mapped[str | None] = mapped_column(String(50))
  middle_name: Mapped[str | None] = mapped_column(String(50))
  google_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
  email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
  email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  phone_number: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
  avatar_url: Mapped[str | None] = mapped_column(Text)

class Roles(Base):
  __tablename__ = 'roles'

  id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String(50))

class ProjectMemberRoles(Base):
  __tablename__ = 'project_member_roles'

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('projects.id'))
  employee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('employees.id'))
  role_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('roles.id'))

class Assignees(Base):
  __tablename__ = 'assignees'

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  task_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('tasks.id'))
  employee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('employees.id'))

class Tags(Base):
  __tablename__ = 'tags'

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String(50))
  task_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('tasks.id'))

class Comments(Base):
  __tablename__ = 'comments'

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  text: Mapped[str] = mapped_column(Text)
  employee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('employees.id'))
  task_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('tasks.id'))
  time: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False
  )
  
class BacklogTasks(Base):
  __tablename__ = 'backlog_tasks'

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String(50))
  description: Mapped[str] = mapped_column(Text)
  project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('projects.id'))

class Statuses(Base):
  __tablename__ = 'statuses'

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String(50))
  project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('projects.id'))