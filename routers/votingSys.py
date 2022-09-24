from typing import List ,Optional
from fastapi import FastAPI , Response ,status ,HTTPException ,Depends ,APIRouter
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=['Vote'])

@router.post('/vote')
def voting(details : schemas.VoteData,db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
        find_user = db.query(models.User).filter(models.User.id == current_user.id).first()
        find_post = db.query(models.Post).filter(models.Post.id == details.post_id).first()
        if not find_user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
        if not find_post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
        if details.direct == 1:
                find_row = db.query(models.Vote).filter(models.Vote.user_id == current_user.id,models.Vote.post_id == details.post_id).all()
                if find_row:
                        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail = " You cannot like a post more than once")
                new_vote= models.Vote(post_id = details.post_id,user_id = current_user.id)   #** is used to unpack the dict
                db.add(new_vote)
                db.commit()
                db.refresh(new_vote)

                return {"details":f"Post with id {details.post_id} Liked!"}
        if details.direct==0:
                row_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id,models.Vote.post_id == details.post_id)
                find_row=row_query.all()
                if not find_row:
                        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail= "Such post does not exist !")
                row_query.delete(synchronize_session=False)
                db.commit()
                return {"msg":"vote deleted"}

        
