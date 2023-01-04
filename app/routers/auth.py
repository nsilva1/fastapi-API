from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserLogin, Token
from ..database_models import User
from ..utils import verify_password
from ..oauth import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

@router.post("/login", response_model=Token)
# using OAuthPasswordRequestForm will required the credentials be sent as form-data
# using UserLogin schema to accept raw JSON payload
async def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    queried_user = db.query(User).filter(User.email == user.username).first()

    if not queried_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not verify_password(user.password, queried_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # create and return token
    access_token = create_access_token(data={"userId":queried_user.id})
    return {"access_token": access_token, "token_type":"Bearer"}