from passlib.context import CryptContext #to secure the password inputted by the user.

#the below line 4 tells passlib the default hashing algo it should follow .
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

def hashing(password: str):
        return pwd_context.hash(password)

def verify(plain_password, hashed_password):
        return pwd_context.verify(plain_password,hashed_password)