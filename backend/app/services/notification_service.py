from sqlalchemy.orm import Session

from models.notification import Notification
from schemas.notification import (
    NotificationCreate,
    NotificationUpdate
)


def get_notifications(db: Session):
    return db.query(Notification).all()


def create_notification(
    db: Session,
    notification: NotificationCreate
):
    db_notification = Notification(
        **notification.model_dump()
    )

    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_notification


def mark_as_sent(
    db: Session,
    notification_id: int
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if not notification:
        return None

    notification.is_sent = True

    db.commit()
    db.refresh(notification)

    return notification


def delete_notification(
    db: Session,
    notification_id: int
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if not notification:
        return False

    db.delete(notification)
    db.commit()

    return True
