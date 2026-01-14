from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeResponse, ResumeVersionResponse
from app.models.user import User
from app.models.resume import Resume, ResumeVersion

router = APIRouter()


@router.post("/", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    resume_data: ResumeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = Resume(
        user_id=current_user.id,
        title=resume_data.title,
        language=resume_data.language,
        template_id=resume_data.template_id,
        content=resume_data.content.model_dump()
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    # Create initial version
    version = ResumeVersion(
        resume_id=resume.id,
        version=1,
        content=resume_data.content.model_dump(),
        source="manual"
    )
    db.add(version)
    db.commit()

    return resume


@router.get("/", response_model=List[ResumeResponse])
async def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return resumes


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return resume


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: UUID,
    resume_data: ResumeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    update_data = resume_data.model_dump(exclude_unset=True)

    if "content" in update_data:
        # Create new version
        new_version = resume.current_version + 1
        version = ResumeVersion(
            resume_id=resume.id,
            version=new_version,
            content=update_data["content"],
            source="manual"
        )
        db.add(version)
        resume.current_version = new_version

    for field, value in update_data.items():
        if field == "content":
            setattr(resume, field, value)
        else:
            setattr(resume, field, value)

    db.commit()
    db.refresh(resume)
    return resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    db.delete(resume)
    db.commit()


@router.get("/{resume_id}/versions", response_model=List[ResumeVersionResponse])
async def list_resume_versions(
    resume_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return resume.versions
