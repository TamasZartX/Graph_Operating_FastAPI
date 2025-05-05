import os
import dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base.metadata.create_all(engine)


def get_db():
    try:
        yield session
    finally:
        session.close()


def creat_graph():
    pass


def delete_node():
    pass
