from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ai_copilot import AICopilotLogModel
from app.schemas.ai_copilot import (
    AICopilotLogCreate,
    AICopilotLogResponse,
)

router = APIRouter(prefix="/ai-copilot", tags=["AI Teacher Copilot & Analytics"])


@router.post(
    "/school/{school_id}",
    response_model=AICopilotLogResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ai_log(
    school_id: int, payload: AICopilotLogCreate, db: Session = Depends(get_db)
):
  # Di sini Anda bisa menyematkan pemanggilan LLM API (Gemini Pro) jika ingin live generate,
  # atau menyimpan log interaksi AI Copilot yang diproses dari service lain.
  new_log = AICopilotLogModel(school_id=school_id, **payload.dict())
  db.add(new_log)
  db.commit()
  db.refresh(new_log)
  return new_log


@router.get("/school/{school_id}", response_model=List[AICopilotLogResponse])
def get_ai_logs_by_school(school_id: int, db: Session = Depends(get_db)):
  return (
      db.query(AICopilotLogModel)
      .filter(AICopilotLogModel.school_id == school_id)
      .all()
  )


@router.get("/teacher/{teacher_id}", response_model=List[AICopilotLogResponse])
def get_ai_logs_by_teacher(teacher_id: int, db: Session = Depends(get_db)):
  return (
      db.query(AICopilotLogModel)
      .filter(AICopilotLogModel.teacher_id == teacher_id)
      .all()
  )


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ai_log(log_id: int, db: Session = Depends(get_db)):
  log = (
      db.query(AICopilotLogModel)
      .filter(AICopilotLogModel.id == log_id)
      .first()
  )
  if not log:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="AI log not found"
    )

  db.delete(log)
  db.commit()
  return None
