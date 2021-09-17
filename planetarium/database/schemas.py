from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    uid: Optional[int]
    name: str
    surname: str
    email: str

    class Config:
        orm_mode = True


class UserList(BaseModel):
    users: List[User]


class UserCreatePlain(User):
    password: str

    class Config:
        orm_mode = True


class UserCreate(User):
    hash: bytes

    class Config:
        orm_mode = True


class Event(BaseModel):
    eid: int
    type: int
    datetime: datetime
    instance_id: int

    class Config:
        orm_mode = True


class Instance(BaseModel):
    iid: Optional[int]
    name: str
    description: str
    owner_id: int
    service_id: int
    owner: Optional[User]
    events: Optional[List[Event]]

    class Config:
        orm_mode = True


class InstanceList(BaseModel):
    instances: List[Instance]


class Service(BaseModel):
    sid: Optional[int]
    name: str
    description: Optional[str]
    banner_filename: Optional[str]
    logo_filename: Optional[str]
    frontend_url: Optional[str]
    project_url: Optional[str]
    discontinued: Optional[bool]
    instances: Optional[List[Instance]]

    class Config:
        orm_mode = True


class ServiceList(BaseModel):
    services: List[Service]
