from sqlalchemy import Column, Integer, String, ForeignKey, event, and_, Table
from sqlalchemy.orm import relationship, foreign, remote, backref

from storage.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    manual_manager = relationship("ManualManager", uselist=False)
    api_managers = relationship("ApiManager")


man_opers_assc = Table('man_opers_assc', Base.metadata,
                       Column('man_manager_id', Integer, ForeignKey('manual_managers.id')),
                       Column('operation_id', Integer, ForeignKey('operations.id'))
                       )

api_opers_assc = Table('api_opers_assc', Base.metadata,
                       Column('api_manager_id', Integer, ForeignKey('api_managers.id')),
                       Column('operation_id', Integer, ForeignKey('operations.id'))
                       )


class ManualManager(Base):
    __tablename__ = "manual_managers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    operations = relationship("Operation", secondary=man_opers_assc)


class ApiManager(Base):
    __tablename__ = "api_managers"

    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    user_id = Column(Integer, ForeignKey("users.id"))

    operations = relationship("Operation", secondary=api_opers_assc)

    __mapper_args__ = {
        "polymorphic_identity": "api_manager",
        "polymorphic_on": type,
    }
