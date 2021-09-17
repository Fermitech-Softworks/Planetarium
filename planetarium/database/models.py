from sqlalchemy import Integer, String, LargeBinary, Column, Boolean, ForeignKey, SmallInteger, DateTime
from sqlalchemy.orm import relationship
from planetarium.database.schemas import User as UserSchema

from planetarium.database.db import Base


class User(Base):
    __tablename__ = "user"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    isAdmin = Column(Boolean, default=True)

    instances = relationship("Instance", back_populates="owner")

    def to_schema(self):
        return UserSchema(uid=self.uid, name=self.name, surname=self.surname, email=self.email)


class Service(Base):
    __tablename__ = "service"

    sid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    banner_filename = Column(String)
    logo_filename = Column(String)
    frontend_url = Column(String, nullable=False)
    project_url = Column(String)
    discontinued = Column(Boolean, default=False)

    instances = relationship("Instance", back_populates="service")


class Instance(Base):
    __tablename__ = "instance"

    iid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    owner = relationship("User", back_populates="instances")
    service = relationship("Service", back_populates="instances")
    events = relationship("Event", back_populates="instance", cascade="all, delete")

    owner_id = Column(Integer, ForeignKey("user.uid"))
    service_id = Column(Integer, ForeignKey("service.sid"))


class Event(Base):
    __tablename__ = "event"

    eid = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(SmallInteger, nullable=False)
    datetime = Column(DateTime, nullable=False)

    instance = relationship("Instance", back_populates="events")

    instance_id = Column(Integer, ForeignKey("instance.iid"), primary_key=True)
