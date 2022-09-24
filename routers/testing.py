from typing import List ,Optional
from fastapi import FastAPI , Response ,status ,HTTPException ,Depends ,APIRouter
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=['testing'])

@router.get('/test')
def tester(db : Session = Depends(get_db)):
        test_query = db.query(models.User)
        print(Depends())
        # print(models.User)
        # print(test_query)
        # print("----")
        # print(test_query.all())
        return {"success"}