from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from storage.database import Base
from storage.models.account import ApiManager


class MonobankApiManager(ApiManager):
    __tablename__ = "monobank_managers"

    id = Column(Integer, ForeignKey("api_managers.id"), primary_key=True)
    token = Column(String)

    operations = relationship("MonobankOperation", back_populates="manager")

    __mapper_args__ = {
        "polymorphic_identity": "monobank_manager"
    }


class MonobankOperation(Base):
    __tablename__ = "monobank_operations"

    id = Column(Integer, primary_key=True)
    bank_id = Column(String)
    unix_time = Column(Integer)
    description = Column(String)
    amount = Column(Integer)
    mcc = Column(Integer)

    manager_id = Column(Integer, ForeignKey("monobank_managers.id"))
    manager = relationship("MonobankApiManager", back_populates="operations")




