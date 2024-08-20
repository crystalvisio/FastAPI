from functools import wraps
from fastapi import HTTPException, status, Depends
from app import models, oauth2


""" 
    Using wrapper for restriction and granting perms to specific Roles
    - admin only wrapper 
    - admin x mod wrapper
    - admin x mod x creator wrapper
    the user role by default has only read_only access.
"""


# Admin Decorator
def admin_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        curr_user: models.User = kwargs.get('curr_user')
        if not curr_user:
            curr_user = Depends(oauth2.get_current_user)

        if curr_user.role.name != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
        
        return function(*args, **kwargs)
    
    return wrapper



# Admin and Mod Decorator
def admin_or_mod(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        curr_user: models.User = kwargs.get('curr_user')
        if not curr_user:
            curr_user = Depends(oauth2.get_current_user)

        if curr_user.role.name not in ["admin", "mod"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
        
        return function(*args, **kwargs)
    
    return wrapper



# Admin, Mod, Creator Decorator
def admin_mod_creator(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        curr_user: models.User = kwargs.get('curr_user')
        if not curr_user:
            curr_user = Depends(oauth2.get_current_user)

        if curr_user.role.name not in ["admin", "mod", "creator"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
        
        return function(*args, **kwargs)
    
    return wrapper

