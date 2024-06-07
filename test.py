from fastapi.testclient import TestClient
from main import app
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from settings import settings
from db.engine import Base, get_db
from main import app
import asyncio
from tests import users

users.test_user_register()