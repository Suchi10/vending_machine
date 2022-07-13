from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.auth_bearer import JWTBearer
from app.config.database import Session, get_session
from app.models.product import Product
from app.schemas.product import ProductBase, ProductCreate, ProductUpdate
from app.utils.product import (
    create_product,
    delete_product,
    fetch_product,
    update_product,
)

router = APIRouter(
    prefix="/product",
    tags=["product"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", dependencies=[Depends(JWTBearer())], status_code=HTTPStatus.CREATED)
def add_product(
    product: ProductBase, session: Session = Depends(get_session)
) -> ProductBase:
    """
    Adds a product to the Product and allocates a product_id.
    """
    product_created = create_product(session, product)
    if product_created:
        return product_created
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="product already exists.",
    )


@router.get(
    "/{product_id}",
    status_code=HTTPStatus.OK,
    response_model=ProductCreate,
    response_model_exclude={"product_id"},
)
async def get_product(
    product_id: int, session: Session = Depends(get_session)
) -> Product:
    """
    Collects all information for a product.
    """
    product_details = fetch_product(session, product_id)
    if product_details is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="product not found.",
        )
    return product_details


@router.put(
    "/{product_id}",
    dependencies=[Depends(JWTBearer())],
    status_code=HTTPStatus.NO_CONTENT,
)
async def update_product_details(
    product_update: ProductUpdate,
    product_id: int,
    seller_id: int,
    session: Session = Depends(get_session),
) -> Product:
    """
    Updates a product information's.
    """
    product_update_details = update_product(
        session, product_id, product_update, seller_id
    )
    if not product_update_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="product not found.",
        )
    return product_update_details


@router.delete(
    "/{product_id}",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product_details(
    product_id: int,
    seller_id: int,
    session: Session = Depends(get_session),
):
    """
    Deletes a product in case seller wants.
    """
    try:
        delete_product(product_id, seller_id, session)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete directory. Please try again later.",
        )
