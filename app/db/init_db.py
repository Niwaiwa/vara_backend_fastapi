import uuid
from sqlalchemy.orm import Session

from app import schemas
from app.models.user_model import User
from app.core.security import get_password_hash
from app.repositories.user_repository import UserRepository

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    username = 'admin'
    email = 'admin@gmail.com'
    hashed_password = get_password_hash('admin')

    user = UserRepository(db).get_by_username(username='admin')
    if not user:
        user_in = schemas.UserCreate(
            username=username,
            email=email,
            password=hashed_password,
            is_superuser=True,
        )
        user = UserRepository(db).create(user_in, hashed_password)  # noqa: F841