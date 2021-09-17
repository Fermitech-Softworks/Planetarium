from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import UploadFile, HTTPException
import bcrypt

from planetarium.database import schemas, models


def get_user(db: Session, uid: int):
    user = db.query(models.User).filter(models.User.uid == uid).first()
    if not user:
        raise HTTPException(404, "Not found.")
    else:
        return user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, name=user.name, surname=user.surname, password=user.hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserCreate, uid: int):
    db_user = get_user(db, uid)
    if not db_user:
        return
    db_user.name = user.name
    db_user.surname = user.surname
    if user.hash:
        db_user.password = user.hash
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user


def get_services(db: Session):
    return db.query(models.Service).all()


def get_service(db: Session, sid: int):
    service = db.query(models.Service).filter(models.Service.sid == sid).first()
    if not service:
        raise HTTPException(404, "Not found.")
    return service


def create_service(db: Session, service: schemas.Service):
    db_service = models.Service(name=service.name, description=service.description,
                                banner_filename=service.banner_filename, logo_filename=service.logo_filename,
                                frontend_url=service.frontend_url, project_url=service.project_url)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def update_service(db: Session, sid: int, update: schemas.Service):
    service: models.Service = get_service(db, sid)
    service.name = update.name
    service.description = update.description
    service.banner_filename = update.banner_filename
    service.logo_filename = update.banner_filename
    service.frontend_url = update.frontend_url
    service.project_url = update.project_url
    service.discontinued = update.discontinued
    db.commit()
    db.refresh(service)
    return service


def get_instance(db: Session, iid:int):
    instance = db.query(models.Instance).filter(models.Instance.iid == iid).first()
    if not instance:
        HTTPException(404, "Not found.")
    return instance


def create_instance(db: Session, instance: schemas.Instance):
    get_user(db, instance.owner_id)
    get_service(db, instance.service_id)
    db_instance = models.Instance(name=instance.name, description=instance.description, owner_id=instance.owner_id,
                                  service_id=instance.service_id)
    db.add(db_instance)
    db.commit()
    db.refresh(db_instance)
    return db_instance


def update_instance(db: Session, iid: int, update: schemas.Instance):
    get_user(db, update.owner_id)
    instance = get_instance(db, iid)
    instance.name = update.name
    instance.description = update.description
    instance.owner_id = update.owner_id
    db.commit()
    db.refresh(instance)
    return instance


def remove_instance(db: Session, iid: int):
    instance = get_instance(db, iid)
    db.delete(instance)
    db.commit()


def create_event(db: Session, event: schemas.Event):
    get_instance(db, event.instance_id)
    db_event = models.Event(type=event.type, datetime=datetime.now())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
