from starlette.responses import JSONResponse
from fastapi import APIRouter
from routes.classes.User import Users
from models.authorizations.frontend.permissions import FrontPermissionModel,FrontUpdatePermissionModel
from middleware import *


router = APIRouter(tags=["authorizations_frontend"])



@router.post('frontend-permissions')
async def create_frontend_permission(PermissionSchema: FrontPermissionModel):
    permissions_obj = Permissions()