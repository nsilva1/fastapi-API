from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, database_models, oauth
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.PostVote, db: Session = Depends(database.get_db), current_user = Depends(oauth.get_current_user)):

    post = db.query(database_models.Post).filter(database_models.Post.id == vote.postId).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post does not exist')

    vote_query = db.query(database_models.Vote).filter(database_models.Vote.postId == vote.postId, database_models.Vote.userId == current_user.id)

    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Vote already exist on this post')
        new_vote = database_models.Vote(postId=vote.postId, userId=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Vote addedd successfully!"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote not found')
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"Vote deleted successfully"}
