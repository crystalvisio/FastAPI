from sqlalchemy.orm import Session
from fastapi import status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app import models, schemas, utils, oauth2, database, decorator


# Initialise App Router
router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    # If the user is not found, no need to verify password
    if not user:
        utils.invalid_credentials()

    # Verify Password
    if not utils.verify_pwd(user_credentials.password, user.password):
        utils.invalid_credentials()

    access_token = oauth2.create_access_token(data={"user_id":user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


# Role Assignment Route (Admin-Only)
@router.put("/assign-role", response_model=schemas.UserBase)
@decorator.admin_only
def assign_role(role_assign:schemas.RoleAssign, db:Session=Depends(database.get_db), curr_user:models.User = Depends(oauth2.get_current_user)):

    # Fetch the user to be assigned a role
    user = db.query(models.User).filter(models.User.id == role_assign.user_id).first()
    if not user:
        raise utils.id_error("User", user.id)
    
    # Fetch the role to assigned
    role = db.query(models.Role).filter(models.Role.name == role_assign.role_name).first()
    if not role:
        raise utils.id_error("Role", role.id)
    
    #Assign new role to the user
    user.role_id = role.id
    db.commit()
    db.refresh(user)

    return user