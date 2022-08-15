from sqlalchemy import Boolean, Column, Integer, String

from db.session import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    hashed_password = Column(String(255),nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)