from jose import JWTError , jwt
from datetime import datetime , timedelta
from . import schemas ,database , models
from .config import settings
from fastapi import Depends,status ,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")

#Secret_Key
#Algo
#Expiration time (Time after which the logged in user will be logged out )

SECRET_KEY = f"{settings.secret_key}"
ALGORITHM = f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
        to_encode = data.copy() #creating copy of data so as to not modify the original data
        expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp":expire})

        encoded_jwt = jwt.encode(to_encode,SECRET_KEY , algorithm=ALGORITHM)
        '''to_encode is the PayLoad , SECRET_KEY is the secret , algorithm is 
        the header for the signature'''

        return encoded_jwt

def verify_access_token(token: str, credentials_exception):
        try: 
                payload =  jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
                uid: str =payload.get("user_id")
                if uid is None:
                        raise credentials_exception
                token_data = schemas.TokenData(id=uid)
        except JWTError:
                raise credentials_exception
        return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
        credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="could not validate the credentials",
                headers={"WWW -Authenticate":"Bearer"})

        token_user = verify_access_token(token,credentials_exception)
        
        user = db.query(models.User).filter(models.User.id == token_user.id).first()
        # print(user)
        return user

'''
Note : so after Login the user will get the access_token from the server.
Now whenever the user wants to tamper or do some activity while being logged-in this token
will be first verified using the get_current_user function .If it returns nothing then everything is fine
and the user can proceed with whatever he/she wants to do . if the exception is returned then the user is a hacker.
'''

        

