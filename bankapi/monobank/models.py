from sqlalchemy import Column, Integer, String, ForeignKey

from storage.models.account import ApiManager
from storage.models.operation import ApiOperation


class MonobankApiManager(ApiManager):
    __tablename__ = "monobank_managers"

    id = Column(Integer, ForeignKey("api_managers.id"), primary_key=True)
    token = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "monobank_manager"
    }


class MonobankOperation(ApiOperation):
    __tablename__ = "monobank_operations"

    id = Column(Integer, ForeignKey('api_operations.id'), primary_key=True)
    bank_id = Column(String)
    unix_time = Column(Integer)
    description = Column(String)
    amount = Column(Integer)
    mcc = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "monobank_opeartion"
    }

