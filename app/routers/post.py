from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import database_models
from ..database import get_db
from typing import List, Optional
from ..schemas import CreatePost, PostApiResponse, PostsWithVotes
from sqlalchemy.orm import Session
from .. import oauth
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/', response_model=List[PostsWithVotes])
async def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    
    # get all posts from the logged in user
    # user_posts = db.query(database_models.Post).filter(database_models.Post.userId == current_user.id).all()

    # get all posts from all users
    # offset used to return data for pagination. array with 10 data objects has offset of 0, page 2 will have offset of 10. etc
    # posts = db.query(database_models.Post).filter(database_models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # join example
    post_with_votes = db.query(database_models.Post, func.count(database_models.Vote.postId).label("Votes") ).join(database_models.Vote, database_models.Vote.postId == database_models.Post.id, isouter=True).group_by(database_models.Post.id).filter(database_models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(post_result)
    return post_with_votes


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostApiResponse)
async def create_post(post: CreatePost, db: Session = Depends(get_db), current_user = Depends(oauth.get_current_user)):
    
    new_post = database_models.Post(userId=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=PostsWithVotes)
async def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth.get_current_user)):
    
    # post = db.query(database_models.Post).filter(database_models.Post.id == id).first()

    post = db.query(database_models.Post, func.count(database_models.Vote.postId).label("Votes") ).join(database_models.Vote, database_models.Vote.postId == database_models.Post.id, isouter=True).group_by(database_models.Post.id).filter(database_models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found") 
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth.get_current_user)):
    
    post_query = db.query(database_models.Post).filter(database_models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Found")

    if post.userId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to delete post")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=PostApiResponse)
async def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db), current_user = Depends(oauth.get_current_user)):
    
    post_query = db.query(database_models.Post).filter(database_models.Post.id == id)

    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Found")

    if post.userId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to edit post")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post
