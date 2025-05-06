import os
import logging
import pytest
import sqlalchemy
from dotenv import load_dotenv
from fastapi.testclient import TestClient

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


from app.main import app
from app import database as db


@pytest.fixture(autouse=True, scope="session")
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,  # или INFO
        format="%(asctime)s [%(levelname)s] %(message)s"
    )


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def clear_db():
    try:
        db.session.close()
    except Exception:
        pass
    db.session = db.SessionLocal()

    with db.engine.begin() as conn:
        conn.execute(sqlalchemy.text("DELETE FROM edge"))
        conn.execute(sqlalchemy.text("DELETE FROM node"))
        conn.execute(sqlalchemy.text("DELETE FROM graph"))
    yield
    db.session.close()
    db.session = db.SessionLocal()
