from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from storage.database import Base


class ManualOperation(Base):
    __tablename__ = "manual_operations"

    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    description = Column(String)
    unix_time = Column(Integer)
    mcc = Column(Integer)
    category = Column(String)

    manager_id = Column(Integer, ForeignKey("manual_managers.id"))
    manager = relationship("ManualManager", back_populates="operations")

