from http import HTTPStatus
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
from app.config.database import Session, get_session
from app.models.user import User
from app.schemas.user import UserBase, UserCreate, UserUpdate
from app.utils.user import create_user, delete_user, fetch_user, update_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
def add_user(user: UserBase, session: Session = Depends(get_session)) -> Dict[str, str]:
    """
    Adds a user to the user and allocates a user_id.
    """
    user_created = create_user(session, user)
    if user_created:
        return signJWT(user.username)
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="user already exists.",
    )


@router.get(
    "/{user_id}",
    dependencies=[Depends(JWTBearer())],
    status_code=HTTPStatus.OK,
    response_model=UserCreate,
    response_model_exclude={"user_id"},
)
async def get_user(user_id: int, session: Session = Depends(get_session)) -> User:
    """
    Collects all information for a input user_id.
    """
    user_details = fetch_user(session, user_id)
    if user_details is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found.",
        )
    return user_details


@router.put(
    "/{user_id}", dependencies=[Depends(JWTBearer())], status_code=HTTPStatus.NO_CONTENT
)
async def update_user_details(
    user_update: UserUpdate,
    user_id: int,
    session: Session = Depends(get_session),
) -> User:
    """
    Takes user_id and updates the active flag to False.
    """
    user_update_details = update_user(session, user_id, user_update)
    if not user_update_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found.",
        )
    return user_update_details


@router.delete(
    "/{user_id}",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_details(
    user_id: int,
    session: Session = Depends(get_session),
):
    """
    Removes all files in the given directory.
    """
    try:
        delete_user(user_id, session)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete directory. Please try again later.",
        )
