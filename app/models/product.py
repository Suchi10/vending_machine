from typing import Optional

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True, nullable=False, index=True
    )
    sellerId: int = Field(nullable=False, index=False)
    amountAvailable: float = Field(nullable=False, index=False)
    cost: float = Field(nullable=False, index=False)
    productName: str = Field(index=False)
