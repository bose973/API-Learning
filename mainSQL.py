# from typing import Optional
# from fastapi import FastAPI , Response ,status ,HTTPException
# from fastapi.params import Body
# from pydantic import BaseModel #to define the schema
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time



# app = FastAPI()

# class Post(BaseModel): #by extending to BasModel it is using pydantic to define our schema
#         # add: int
#         title: str
#         content: str 
#         published: bool = True

# #RealDictCursor is used to fetch the column name as well
# while True:
#         try:
#                 conn=psycopg2.connect(host='localhost',database='learnAPI',user='postgres',
#                 password='sid123', cursor_factory=RealDictCursor)
#                 cursor=conn.cursor()
#                 print("DataBase connection was successful!")
#                 break
#         except Exception as error:
#                 print("Connecting failed")
#                 print(f"Error was {error}")
#                 time.sleep(3) 


# my_posts=[{"title":"title of post1", "content":"content of post1","id":1},
# {"title":"favourite foods","content":"I like chicken","id":2}]



# # path operation
# @app.get("/")     #this decorator makes the functions work as api ,get() is the http method we used
# def root():           #This function will have the code that we want to operate
#     return {"message": "Welcome siddhartha bose"} #whatever we return here will be sent back to user in the website.
#                                       #This return value is converted to JSON , it is the univeral language of API 

# #defining above path operation
# '''
# get is the "HTTP Method"
# root is the "function"
# inside the get method is the path
# ''' 

# #get all the posts.
# @app.get("/posts")
# def get_posts():
#         cursor.execute("""SELECT * FROM posts;""")
#         posts=cursor.fetchall()
#         return {"data":posts}

# # extracting data from directly the body
# # @app.post("/createposts")
# # def ceate_posts(payLoad: dict = Body(...)):
# #         print(payLoad)
# #         return {"new_post":f"title : {payLoad['title']} , content : {payLoad['content']}"}


# #so here are creating new post using the pydantic schema data input from postman body
# @app.post("/posts")
# def ceate_posts(post: Post,response : Response):
#         cursor.execute("""INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING *;""",
#         (post.title,post.content))
#         new_post=cursor.fetchone()

#         #the above code makes safe from SQL injection
#         # print(post.rating)
#         # print(post.dict())
#         # post.add=post.add*2
#         # post_dict=post.dict()
#         # post_dict['id']=randrange(0,10000000)
#         # my_posts.append(post_dict)
#         # response.status_code=201
#         conn.commit() #to finalize the changes to the postgres database.
#         return {"data": new_post}
#         # return {"title" : f"{post.title}" , "content" : f"{post.content}","published":f"{post.published}"}

# #title str , content str

# def find_post(id):
#         for posts in my_posts:
#                 # print(type(posts['id']),type(id))
#                 if int(id) == posts['id']:
#                         return posts
#         return {}

# #finding post from the SQL Server Postgres        
# def findPost(id):
#         cursor.execute("""SELECT * FROM posts WHERE id=%s; """,(str(id)))
#         post=cursor.fetchone()
#         return post

# #creating a method to fetch individual post using id.
# #id field is the path parameter
# @app.get('/posts/{id}')
# def get_post(id: int,response: Response):
#         print(id)
#         p=findPost(id)
#         # p=find_post(id)
#         if not p:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
#                 # response.status_code=status.HTTP_404_NOT_FOUND 
#                 # return {"message":f"post with id {id} was not found"}
#         return {"data":p}



# #deleting a post
# @app.delete('/posts/{id}')
# def delete_post(id: int,r: Response):
#         # p=find_post(id)
#         # for i in range(len(my_posts)):
#         #         if p==my_posts[i]:
#         #                 my_posts.pop(i)
#         #                 return Response(status_code=204)

#         cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""",(str(id),))
#         deleted_post=cursor.fetchone()
        
#         if not deleted_post:
#                 raise HTTPException(status_code=404,detail=f"Post with id {id} does not exist")
#         conn.commit()
#         return Response(status_code=204)
        



# #creating a method to update a post
# @app.put('/posts/{id}')
# def update_post(id: int,uPost: Post):
#         # p=find_post(id)
#         # if p=={}:
#         #         raise HTTPException(status_code=404,detail=f"Post with the id {id} does not exist")
#         # u=uPost.dict()
#         # p['title']=u['title']
#         # p['content']=u['content']
#         cursor.execute("""UPDATE posts SET title=%s,content=%s WHERE id = %s RETURNING *;""",(uPost.title
#         ,uPost.content,str(id)))
#         updated_post=cursor.fetchone()
#         if not updated_post:
#                 raise HTTPException(status_code=404,detail=f"Post with the id {id} does not exist")
                
#         conn.commit()
#         return {"details":"post updated","updated_post data":updated_post}

        



