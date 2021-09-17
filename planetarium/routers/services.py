from fastapi import APIRouter, Depends, HTTPException
from planetarium.dependencies import get_db
from planetarium.authentication import get_current_user, check_admin
from planetarium.database.crud import create_service, get_service, get_services, update_service
from sqlalchemy.orm import Session
from planetarium.database import schemas, models
from typing import Optional


router = APIRouter(
    prefix="/service",
    tags=["services"],
    responses={404: {"description": "Not found"}, 204: {"description": "Removed"}, 401: {"description": "Not authenticated"},
               403: {"description": "Not authorized"}}
)


@router.get("/", tags=["services"], response_model=schemas.ServiceList)
async def read_service_list(service_id: Optional[int] = None, db: Session = Depends(get_db)):
    if service_id:
        service = get_service(db, service_id)
        return schemas.ServiceList(services=[service, ])
    return schemas.ServiceList(services=get_services(db))


@router.post("/", tags=["services"], response_model=schemas.Service)
async def post_service(service: schemas.Service, db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)):
    if not check_admin(current_user):
        raise HTTPException(403, "Not authorized.")
    return create_service(db, service)


@router.patch("/", tags=["services"], response_model=schemas.Service)
async def patch_service(service: schemas.Service, service_id: int ,db: Session = Depends(get_db),
                        current_user: models.User = Depends(get_current_user)):
    if not check_admin(current_user):
        raise HTTPException(403, "Not authorized.")
    return update_service(db, service_id, service)
