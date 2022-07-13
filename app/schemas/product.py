from pydantic import BaseModel


class ProductBase(BaseModel):
    sellerId: int
    amountAvailable: float
    cost: float
    productName: str


class ProductCreate(ProductBase):
    ...


class ProductUpdate(BaseModel):
    amountAvailable: float
    cost: float
    productName: str
