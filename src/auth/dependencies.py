from fastapi import Depends, Request
from .permissions import AdminPermission, AuthorOrAdminPermission, CurrentUserOrAdminPermission, CurrentUserPermission
from .service import CurrentUser, get_current_user
from .models import User


async def admin_permission(request: Request, user: CurrentUser):
    permission = AdminPermission(request=request, user=user)
    permission()
    return user

async def current_user(request: Request, user: CurrentUser):
    permission = CurrentUserPermission(request=request, user=user)
    permission()
    return user

async def current_user_or_admin(request: Request, user: CurrentUser):
    permission = CurrentUserOrAdminPermission(request=request, user=user)
    permission()
    return user

async def author_or_admin_permissasion(request: Request, user: CurrentUser):
    permission = AuthorOrAdminPermission(request=request, user=user)
    permission()
    return user
