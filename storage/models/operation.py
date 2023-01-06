from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from storage.database import Base


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    # two types: man - manual | api - from API
    type = Column(String(3))

    manual_operation = relationship("ManualOperation", back_populates="operation", uselist=False)
    api_operation = relationship("ApiOperation", back_populates="operation", uselist=False)

    @property
    def current_operation(self):
        types = {
            "man": self.manual_operation,
            "api": self.api_operation
        }
        return types[self.type]


class ManualOperation(Base):
    __tablename__ = "manual_operations"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    description = Column(String)
    unix_time = Column(Integer)
    mcc = Column(Integer)
    category = Column(String)

    operation_id = Column(Integer, ForeignKey("operations.id"))
    operation = relationship("Operation", back_populates="manual_operation")


class ApiOperation(Base):
    __tablename__ = "api_operations"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String)

    # FK to Operation model
    operation_wrapper_id = Column(Integer, ForeignKey("operations.id"))
    operation = relationship("Operation", back_populates="api_operation")

    type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "api_operation",
        "polymorphic_on": type,
    }

