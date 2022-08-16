from sqlalchemy import Column, Integer, String

from db.session import Base

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    role_name = Column(String(255), nullable=False, index=True)
