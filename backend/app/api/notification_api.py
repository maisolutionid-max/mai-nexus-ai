from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schemas.notification import (
    NotificationCreate,
    NotificationResponse
)

from services.notification_service import (
    get_notifications,
    create_notification,
    mark_as_sent,
    delete_notification
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get(
    "/",
    response_model=list[NotificationResponse]
)
def read_notifications(
    db: Session = Depends(get_db)
):
    return get_notifications(db)


@router.post(
    "/",
    response_model=NotificationResponse
)
def create(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    return create_notification(
        db,
        notification
    )


@router.put("/{notification_id}/sent")
def sent(
    notification_id: int,
    db: Session = Depends(get_db)
):
    result = mark_as_sent(
        db,
        notification_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return result


@router.delete("/{notification_id}")
def delete(
    notification_id: int,
    db: Session = Depends(get_db)
):
    result = delete_notification(
        db,
        notification_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return {
        "message": "Notification deleted successfully"
}
