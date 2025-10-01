from functools import wraps
from fastapi import HTTPException, status
import inspect

from app.models.user import User


def require_role(allowed_roles: list[str]):

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, current_user: User = None, **kwargs):
            if current_user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not authenticated",
                )
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access forbidden: requires role(s) {', '.join(allowed_roles)}",
                )

            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs, current_user=current_user)
            else:
                return func(*args, **kwargs, current_user=current_user)

        return async_wrapper

    return decorator
