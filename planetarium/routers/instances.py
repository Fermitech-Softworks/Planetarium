from fastapi import APIRouter, Depends, Request, File, UploadFile, Form, HTTPException
from planetarium.dependencies import get_auth_token, get_db, save_file
from planetarium.authentication import get_current_user, check_admin
from planetarium.database.crud import create_instance, get_instance, update_instance, remove_instance
from sqlalchemy.orm import Session
from planetarium.database import schemas, models

router = APIRouter(
    prefix="/instance",
    tags=["instances"],
    responses={404: {"description": "Not found"}, 204: {"description": "Removed"},
               401: {"description": "Not authenticated"},
               403: {"description": "Not authorized"}}
)


@router.post("/", tags=["instances"], response_model=schemas.Instance)
async def post_instance(instance: schemas.Instance, db: Session = Depends(get_db),
                        current_user: models.User = Depends(get_current_user)):
    if not check_admin(current_user):
        raise HTTPException(403, "Not authorized.")
    return create_instance(db, instance)


@router.patch("/", tags=["instances"], response_model=schemas.Instance)
async def patch_instance(update: schemas.Instance, instance_id: int, db: Session = Depends(get_db),
                         current_user: models.User = Depends(get_current_user)):
    instance: models.Instance = get_instance(db, instance_id)
    if current_user.uid != instance.owner_id and not check_admin(current_user):
        raise HTTPException(403, "Not authorized.")
    return update_instance(db, instance_id, update)


@router.delete("/", tags=["instances"])
async def delete_instance(instance_id: int, db: Session = Depends(get_db),
                          current_user: models.User = Depends(get_current_user)):
    if not check_admin(current_user):
        raise HTTPException(403, "Not authorized.")
    remove_instance(db, instance_id)
    raise HTTPException(204, "Removed.")
