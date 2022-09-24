from fastapi import APIRouter ,Depends , status ,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database , schemas ,utils ,models, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model= schemas.Token)
def login(cred: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):
        email=cred.username
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
                raise HTTPException(status_code=403,detail="Invalid Credentials")
        if not utils.verify(cred.password,user.password):
                raise HTTPException(status_code=403,detail="Invalid Credentials")

        #create a token , then return the token
        
        access_token = oauth2.create_access_token(data= {"user_id": user.id}) #data is the payload

        return {"access_token" : access_token , "token_type" :"bearer"}


