from fastapi import FastAPI , Response ,status ,HTTPException ,Depends ,APIRouter
from .. import models,schemas , utils ,oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
        prefix = "/register" ,
        tags = ["Users"]
)

@router.post('/',status_code=201,response_model=schemas.UserResp)
def create_user(reg: schemas.UserCreate , db: Session = Depends(get_db)):
        #hash the password - reg.password ..so that password is secured.
        hashed_password = utils.hashing(reg.password)
        reg.password=hashed_password

        new_user= models.User(**reg.dict()) #** is used to unpack the dict
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

@router.get('/{id}',status_code=200, response_model = schemas.UserResp)
def get_user(id : int , db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
        user= db.query(models.User).filter(models.User.id == id).first()
        if not user:
                raise HTTPException(status_code=404, detail=f"user with id {id} does not exist")
        return user
        