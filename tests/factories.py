from typing import Optional, Type

import factory
from factory.alchemy import SQLAlchemyModelFactory
from factory.faker import faker
from sqlmodel import Session

from app.models.product import Product

FAKE = faker.Faker()


class BaseFactory(SQLAlchemyModelFactory):
    @classmethod
    def set_factories_session(
        cls, session: Session, class_: Optional[Type["BaseFactory"]] = None
    ) -> None:
        if class_ is None:
            class_ = cls
        class_._meta.sqlalchemy_session = session
        for subclass in class_.__subclasses__():
            cls.set_factories_session(session, subclass)


class ProductFactory(BaseFactory):
    class Meta:
        model = Product

    id = factory.Faker("random_int", min=1, max=100)
    sellerId = factory.Faker("random_int", min=1, max=100)
    amountAvailable = "10.0"
    cost = "12.0"
    productName = factory.Faker("text", max_nb_chars=20)
