from sqlalchemy import ForeignKey, String, Boolean, Column, Integer, Date, DateTime, func, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import List, Optional
import uuid
from database import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[int] = mapped_column(Numeric, nullable=False)
    start_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)

    # relationship with 'tasks' table
    tasks: Mapped[List['Task']] = relationship('Task', back_populates='project', lazy='selectin')

    # relationship with 'issues' table
    issues: Mapped[List['Issue']] = relationship('Issue', back_populates='project',lazy='selectin')

class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    globalid: Mapped[str] = mapped_column(String, nullable=False)
    expressid: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Numeric, nullable=False)
    start_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)

    # Relationship with User
    user_issued_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    issued_task_by: Mapped["User"] = relationship("User", foreign_keys=[user_issued_id], back_populates="issued_task", lazy='joined')

    # Relationship with User
    user_assign_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    assigned_task_to: Mapped["User"] = relationship("User", foreign_keys=[user_assign_id], back_populates="assigned_task", lazy='joined')
    
    
    # Relationship with task_activities
    activities_for_tasks: Mapped[List["TaskActivity"]] = relationship("TaskActivity", back_populates="task", lazy='joined')

    # Relationship with projects
    project_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    project: Mapped['Project'] = relationship("Project", foreign_keys=[project_id] , back_populates="tasks", lazy='joined')
    


class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    level: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
    photo: Mapped[str] = mapped_column(String, nullable=True)

    # Relationship with task
    issued_task: Mapped[List['Task']] = relationship('Task', back_populates='issued_task_by', lazy='selectin')
    assigned_task: Mapped[List['Task']] = relationship('Task', back_populates='assigned_task_to', lazy='selectin')

    # Relationship with issue
    issued_issue: Mapped[List['Issue']] = relationship('Issue', back_populates='issued_issue_by', lazy='selectin')
    assigned_issue: Mapped[List['Issue']] = relationship('Issue', back_populates='assigned_issue_to', lazy='selectin')

    # Relationship with task_activity
    user_activity_task: Mapped[List['TaskActivity']] = relationship('TaskActivity', back_populates='update_task_by', lazy='joined')

    # Relationship with issue_activity
    user_activity_issue: Mapped[List['IssueActivities']] = relationship('IssueActivities', back_populates='update_issue_by', lazy='selectin')

    # Relation with track document
    user_upload_document: Mapped[List["TrackDocument"]] = relationship("TrackDocument", back_populates="upload_document_by", lazy="selectin")

    # Relation with modified document
    user_modified_document: Mapped[List["ModifiedDocument"]] = relationship("ModifiedDocument", back_populates="user_modified", lazy='selectin')

    # Relation with library
    user_upload_library: Mapped[List["Library"]] = relationship("Library", back_populates="upload_library_by", lazy='selectin')


class TaskActivity(Base):
    __tablename__ = 'task_activities'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity: Mapped[str] = mapped_column(String, nullable=False)
    date_activity: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())
    photo: Mapped[str] = mapped_column(String, nullable=True)

    # Foreign Key (Define before relationship)
    task_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)

    # Relationship with TaskActivities
    task: Mapped["Task"] = relationship("Task", back_populates="activities_for_tasks", lazy='selectin')

    # Relationship with user
    user_task_activities_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    update_task_by: Mapped["User"] = relationship("User", foreign_keys=[user_task_activities_id], back_populates="user_activity_task", lazy='selectin')

class Issue(Base):
    __tablename__ = 'issues'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    globalid: Mapped[str] = mapped_column(String, nullable=False)
    expressid: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String,nullable=False)
    description: Mapped[str] = mapped_column(String,nullable=True)
    photo: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    date_issued: Mapped[Date] = mapped_column(Date, nullable=False, default=func.now())
    closed_date: Mapped[Date] = mapped_column(Date, nullable=True)

    # Relationship withj user
    user_issued_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    issued_issue_by: Mapped["User"] = relationship("User", foreign_keys=[user_issued_id], back_populates="issued_issue", lazy='selectin')
    user_assign_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    assigned_issue_to: Mapped["User"] = relationship("User", foreign_keys=[user_assign_id], back_populates="assigned_issue", lazy='selectin')

    # Relationship with project
    project_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    project: Mapped["Project"] = relationship("Project", foreign_keys=[project_id] , back_populates="issues", lazy='selectin')
    

    # Relationship with issue_activities
    activities_for_issue: Mapped[List["IssueActivities"]] = relationship("IssueActivities", back_populates="issue", lazy='selectin')
    

class IssueActivities(Base):
    __tablename__ = 'issue_activities'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity: Mapped[str] = mapped_column(String, nullable=False)
    date_activity: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())
    photo: Mapped[str] = mapped_column(String, nullable=True)
    
    # Relationship with table issues
    issue_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('issues.id'), nullable=False)
    issue: Mapped["Issue"] = relationship("Issue", foreign_keys=[issue_id] , back_populates="activities_for_issue", lazy='selectin')

    # Relationship with user
    user_issue_activities_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    update_issue_by: Mapped["User"] = relationship("User", foreign_keys=[user_issue_activities_id] , back_populates="user_activity_issue", lazy='selectin')

class TrackDocument(Base):
    __tablename__ = 'track_documents'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    date_document: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())

    # Relation with user
    upload_user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    upload_document_by: Mapped["User"] = relationship("User", foreign_keys=[upload_user_id], back_populates="user_upload_document")

    # Relation with modified document
    user_modified_document: Mapped[List["ModifiedDocument"]] = relationship("ModifiedDocument", back_populates="track_document", lazy='selectin')

class ModifiedDocument(Base):
    __tablename__ = 'modified_documents'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    track_document_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('track_documents.id'), nullable=False)

    # Relationship with Track Document
    track_document: Mapped["TrackDocument"] = relationship("TrackDocument", foreign_keys=[track_document_id], back_populates="user_modified_document" , lazy='selectin')
    modified_document: Mapped[str] = mapped_column(String, nullable=False)

    date_modified_document: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())

    # Relationship with User
    user_modified_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    user_modified: Mapped["User"] = relationship("User", foreign_keys=[user_modified_id], back_populates="user_modified_document" , lazy='selectin')

class Library(Base):
    __tablename__ = 'library'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    date_library: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())

    # Relation with User
    upload_library_user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    upload_library_by: Mapped["User"] = relationship("User", foreign_keys=[upload_library_user_id], back_populates="user_upload_library", lazy='selectin')