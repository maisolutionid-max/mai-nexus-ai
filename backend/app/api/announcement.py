from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.announcement import AnnouncementModel
from app.schemas.announcement import (
    AnnouncementCreate,
    AnnouncementResponse,
    AnnouncementUpdate,
)

router = APIRouter(prefix="/announcements", tags=["School Announcements"])


@router.post(
    "/",
    response_model=AnnouncementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_announcement(
    payload: AnnouncementCreate, db: Session = Depends(get_db)
):
  # Asumsi school_id diambil dari payload atau konteks user/guru
  # Untuk MVP, kita sediakan school_id langsung atau pastikan ikut di-input
  # Mari kita cek apakah model membutuhkan school_id di payload schemas.
  # Di schema base kita tidak ada school_id eksplisit, jadi kita bisa ambil dari relasi teacher jika ada,
  # atau menambahkan school_id di schema. Agar fleksibel, kita set dari payload jika ada, atau default.
  # Mari buat aman: pastikan payload memiliki school_id atau diambil dari teacher.
  pass
  
