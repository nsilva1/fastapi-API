from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import database_models, utils
from ..database import get_db
from ..schemas import CreateUser, CreateUserApiResponse
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=CreateUserApiResponse)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = utils.hash_password(user.password)
    # store hashed password in user.password
    user.password = hashed_password

    new_user = database_models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=CreateUserApiResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    user = db.query(database_models.User).filter(database_models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found") 
    return user
