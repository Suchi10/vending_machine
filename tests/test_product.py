from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.routes.product import router
from tests.factories import ProductFactory

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def setup_product(session: Session) -> None:
    ProductFactory(id=1)
    session.commit()


payload = {"sellerId": 1, "amountAvailable": 12.0, "cost": 10.0, "productName": "Table"}


def test_get_product(session: Session) -> None:
    setup_product(session)
    session.commit()
    response = client.get(f"/product/1")
    assert response.status_code == status.HTTP_200_OK


def test_get_invalid_product(session: Session) -> None:
    setup_product(session)
    session.commit()
    response = client.get(f"/product/1000")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "product not found."}


def test_add_product_not_authenticated(session: Session) -> None:
    session.commit()
    response = client.post("/product/", json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_product_not_authenticated(session: Session) -> None:
    setup_product(session)
    input_update = {"amountAvailable": 121.0, "cost": 110.0, "productName": "Table_new"}
    session.commit()
    response = client.put(f"/product/{1}{1}", json=input_update)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_product_not_authenticated(session: Session) -> None:
    setup_product(session)
    session.commit()
    response = client.delete(f"/product/{1}{1}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
