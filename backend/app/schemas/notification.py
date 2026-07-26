from pydantic import BaseModel


class NotificationCreate(BaseModel):
    title: str
    message: str
    recipient: str
    channel: str = "system"


class NotificationUpdate(BaseModel):
    is_sent: bool


class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    recipient: str
    channel: str
    is_sent: bool

    class Config:
        from_attributes = True
