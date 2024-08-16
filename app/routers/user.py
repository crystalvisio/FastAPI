from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas, utils, database,oauth2


# Initialise App Router
router = APIRouter(
    prefix="/user",
    tags=["User"]
)

# Role Assignment Route (Admin-Only)
@router.put("/assign-role/{user_id}", response_model=schemas.UserBase)
def assign_role(role_assign:schemas.RoleAssign, db:Session=Depends(database.get_db), curr_user:models.User = Depends(oauth2.get_current_user)):
    # Ensure the current user is admin
    if curr_user.role.name != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")

    # Fetch the user to be assigned a role
    user = db.query(models.User).filter(models.User.id == role_assign.user_id).first()
    if not user:
        raise utils.id_error
    
    # Fetch the role to assigned
    role = db.query(models.Role).filter(models.Role.name == role_assign.role_name).first()
    if not role:
        raise utils.id_error
    
    #Assign new role to the user
    user.role_id = role.id
    db.commit()
    db.refresh(user)

    return user

# Creating User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserBase)
def create_users(user:schemas.UserCreate, db: Session = Depends(database.get_db)):

    # hashing pwd - user.password
    user.password = utils.hash_pwd(user.password)

    # Assign a default user role during account creation
    default_role = db.query(models.Role).filter(models.Role.name == "user").first()

    new_user = models.User(**user.model_dump(), role_id = default_role.id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # return  new user

    return new_user


# Getting User by id
@router.get("/{id}", response_model=schemas.UserGet)
def get_users(id:int, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.id==id).first()

    if not user:
        utils.id_error("User", id)

    return user