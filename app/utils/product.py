import logging
from typing import List, Optional, Union

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.product import Product
from app.schemas.product import ProductBase, ProductCreate, ProductUpdate


def create_product(session: Session, product: ProductBase) -> ProductCreate:
    """
    Checks for product existence or creates new.
    """
    try:
        db_product = ProductCreate(
            sellerId=product.sellerId,
            amountAvailable=product.amountAvailable,
            cost=product.cost,
            productName=product.productName,
        )
        session.add(db_product)
        session.commit()
        return db_product
    except Exception as error_caught:
        logging.error(error_caught.args)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: unable to create product, {error_caught.args}",
        ) from error_caught


def fetch_product(session: Session, product_id: int) -> Optional[Product]:
    """
    Fetches product details if exists.
    """
    data_collected = select(Product).where(Product.id == product_id)
    data_execute = session.exec(data_collected).one_or_none()
    return data_execute


def update_product(
    session: Session,
    product_id: int,
    product_update: ProductUpdate,
    seller_id: int,
) -> Union[Product, None]:
    """
    Updates a product's information.
    """
    get_record_update = fetch_product(session, product_id)
    if get_record_update is not None:
        if get_record_update.sellerId == seller_id:
            get_record_update.productName = product_update.productName
            session.commit()
        return get_record_update
    return None


def delete_product(
    product_id: int,
    seller_id: int,
    session: Session,
) -> Union[Product, None]:
    """
    Delete a product.
    """
    get_record_delete = fetch_product(session, product_id)
    if get_record_delete is not None:
        if get_record_delete.sellerId == seller_id:
            session.delete(product_id)
            session.commit()
        return get_record_delete
    return None
