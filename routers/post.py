from typing import List ,Optional
from fastapi import FastAPI , Response ,status ,HTTPException ,Depends ,APIRouter
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router=APIRouter(
        # prefix = "/posts",
        tags = ['Posts']
)

#  "Post": {
#             "title": "post of boat",
#             "content": " been enrolled with ABC",
#             "created_at": "2022-08-18T16:55:09.250656+05:30",
#             "published": true,
#             "id": 9,
#             "owner_id": 15
#         },
#         "votes": 0
#     },


#get all the posts.
@router.get("/posts" , response_model = List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user),
limit : int =10 ,skip : int = 0,search : Optional[str] = "" ):
        # cursor.execute("""SELECT * FROM posts;""")
        # posts=cursor.fetchall()
        posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        results = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id == models.Vote.post_id,isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        #above join means LEFT INNER join..we wnat OUTER Join so we modify
        return results

# extracting data from directly the body
# @router.post("/createposts")
# def ceate_posts(payLoad: dict = Body(...)):
#         print(payLoad)
#         return {"new_post":f"title : {payLoad['title']} , content : {payLoad['content']}"}


#so here are creating new post using the pydantic schema data input from postman body
@router.post("/posts",status_code=201,response_model=schemas.PostResp)
def create_posts(postR: schemas.CreatePost, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): 
        # cursor.execute("""INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING *;""",
        # (post.title,post.content))
        # new_post=cursor.fetchone()
        
        # print(current_user.id)
        # new_post= models.Post(title=post.title,content=post.content)
        
        new_post= models.Post(owner_id = current_user.id,**postR.dict())   #** is used to unpack the dict
        db.add(new_post)
        db.commit()
        db.refresh(new_post) #to retrieve (just like returning in raw sql)
        return new_post
        #the above code makes safe from SQL injection
        # print(post.rating)
        # print(post.dict())
        # post.add=post.add*2
        # post_dict=post.dict()
        # post_dict['id']=randrange(0,10000000)
        # my_posts.append(post_dict)
        # response.status_code=201
        # conn.commit() #to finalize the changes to the postgres database.
        
        # return {"title" : f"{post.title}" , "content" : f"{post.content}","published":f"{post.published}"}

#title str , content str


#creating a method to fetch individual post using id.
#id field is the path parameter
@router.get('/posts/{id}', response_model = schemas.PostVote)
def get_post(id: int,response: Response,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        # print(id)
        # p=findPost(id)
        p1=db.query(models.Post).filter(models.Post.id == id).first()
        p=db.query(models.Post , func.count(models.Vote.post_id).label('votes')).join(models.Vote ,models.Post.id == models.Vote.post_id,isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
        # p=find_post(id)
        
        if not p:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
                # response.status_code=status.HTTP_404_NOT_FOUND 
                # return {"message":f"post with id {id} was not found"}
        return p



#deleting a post
@router.delete('/posts/{id}')
def delete_post(id: int,r: Response,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        # p=find_post(id)
        # for i in range(len(my_posts)):
        #         if p==my_posts[i]:
        #                 my_posts.pop(i)
        #                 return Response(status_code=204)

        # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""",(str(id),))
        # deleted_post=cursor.fetchone()


        post=db.query(models.Post).filter(models.Post.id == id)
        
        
        if not post.first():
                raise HTTPException(status_code=404,detail=f"Post with id {id} does not exist")

        if post.first().owner_id != current_user.id:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "Not Authorized to requested action")


        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=204)
        



#creating a method to update a post
@router.put('/posts/{id}',response_model= schemas.PostResp)
def update_post(id: int,uPost: schemas.PostBase,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        # p=find_post(id)
        # if p=={}:
        #         raise HTTPException(status_code=404,detail=f"Post with the id {id} does not exist")
        # u=uPost.dict()
        # p['title']=u['title']
        # p['content']=u['content']
        # cursor.execute("""UPDATE posts SET title=%s,content=%s WHERE id = %s RETURNING *;""",(uPost.title
        # ,uPost.content,str(id)))
        # updated_post=cursor.fetchone()
        post=db.query(models.Post).filter(models.Post.id==id)
        
        if not post.first():
                raise HTTPException(status_code=404,detail=f"Post with the id {id} does not exist")

        if post.first().owner_id != current_user.id:
                raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "Not Authorized to requested action")
        # conn.commit()
        # post.update({'title':uPost.title,'content':uPost.content},synchronize_session=False)
        post.update(uPost.dict(),synchronize_session=False)
        db.commit()
        return post.first()

        #sdsid@222  sa32@gmail.com
        #sd223