import logging
from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.config.security import get_password_hash
from app.models.user import User, UserRole
from app.schemas.user import UserBase, UserCreate, UserUpdate


def create_user(session: Session, user: UserBase) -> User:
    """
    Checks for user existence or creates new.
    """
    try:
        hashed_password = get_password_hash(user.password)
        role = UserRole[user.role]
        db_user = User(
            username=user.username,
            password=hashed_password,
            deposit=user.deposit,
            role=role,
        )
        session.add(db_user)
        session.commit()
        return db_user
    except Exception as error_caught:
        logging.error(error_caught.args)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: unable to create user, {error_caught.args}",
        ) from error_caught


def fetch_user(session: Session, user_id: int) -> Optional[User]:
    """
    Fetches user details if exists.
    """
    data_collected = select(User).where(User.id == user_id)
    data_execute = session.exec(data_collected).one_or_none()
    return data_execute


def update_user(
    session: Session, user_id: int, user_update: UserUpdate
) -> Optional[User]:
    """
    Updates a user's active status.
    """
    get_record_update = fetch_user(session, user_id)
    if get_record_update is not None:
        get_record_update.userName = user_update
        session.commit()
    return get_record_update


def delete_user(
    user_id: int,
    session: Session,
) -> Optional[User]:
    """
    Updates a user's active status.
    """
    get_record_delete = fetch_user(session, user_id)
    if get_record_delete is not None:
        session.delete(user_id)
        session.commit()

    return get_record_delete
