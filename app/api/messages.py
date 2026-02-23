from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..schemas import MessageCreate
from .auth import get_current_user

router = APIRouter()


@router.post("/send-message")
def send_message(msg: MessageCreate,
                 db: Session = Depends(get_db),
                 current_user: models.User = Depends(get_current_user)):

    new_message = models.Message(
        sender_id=current_user.id,
        receiver_id=msg.receiver_id,
        content=msg.content
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return {"message": "Message sent"}


@router.get("/messages/{user_id}")
def get_messages(user_id: int,
                 db: Session = Depends(get_db),
                 current_user: models.User = Depends(get_current_user)):

    messages = db.query(models.Message).filter(
        ((models.Message.sender_id == current_user.id) & (models.Message.receiver_id == user_id)) |
        ((models.Message.sender_id == user_id) & (models.Message.receiver_id == current_user.id))
    ).all()

    return messages
