from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from storage.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    manual_manager = relationship("ManualManager", uselist=False)
    api_managers = relationship("ApiManager")


class ManualManager(Base):
    __tablename__ = "manual_managers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    operations = relationship("ManualOperation", back_populates="manager")


class ApiManager(Base):
    __tablename__ = "api_managers"

    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    user_id = Column(Integer, ForeignKey("users.id"))

    __mapper_args__ = {
        "polymorphic_identity": "api_manager",
        "polymorphic_on": type,
    }
