import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.config import settings
from tests.factories import BaseFactory

engine = create_engine(settings.DATABASE_URL)


@pytest.fixture
def session() -> Session:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as current_session:
        BaseFactory.set_factories_session(current_session)
        yield current_session
    SQLModel.metadata.drop_all(engine)
