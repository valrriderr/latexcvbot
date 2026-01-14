from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.models.resume import ResumeLanguage


class PersonalInfo(BaseModel):
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: Optional[str] = None
    website: Optional[str] = None
    summary: Optional[str] = None


class WorkExperience(BaseModel):
    company: str
    position: str
    location: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    is_current: bool = False
    description: Optional[str] = None
    achievements: List[str] = []


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    location: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    achievements: List[str] = []


class Skill(BaseModel):
    name: str
    level: Optional[str] = None  # beginner, intermediate, advanced, expert


class Language(BaseModel):
    name: str
    proficiency: str  # native, fluent, advanced, intermediate, basic


class ResumeContent(BaseModel):
    personal_info: PersonalInfo = PersonalInfo()
    work_experience: List[WorkExperience] = []
    education: List[Education] = []
    skills: List[Skill] = []
    languages: List[Language] = []


class ResumeCreate(BaseModel):
    title: str = "Untitled Resume"
    language: ResumeLanguage = ResumeLanguage.EN
    template_id: str = "default"
    content: ResumeContent = ResumeContent()


class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    language: Optional[ResumeLanguage] = None
    template_id: Optional[str] = None
    content: Optional[ResumeContent] = None


class ResumeResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    language: ResumeLanguage
    template_id: str
    content: ResumeContent
    current_version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResumeVersionResponse(BaseModel):
    id: UUID
    resume_id: UUID
    version: int
    content: ResumeContent
    source: str
    created_at: datetime

    class Config:
        from_attributes = True
