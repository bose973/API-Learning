
from fastapi import FastAPI 
from . import models
from .database import engine
from .routers import post,user,auth,votingSys,testing
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# my_posts=[{"title":"title of post1", "content":"content of post1","id":1},
# {"title":"favourite foods","content":"I like chicken","id":2}]

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votingSys.router)
app.include_router(testing.router)


# def find_post(id):
#         for posts in my_posts:
#                 # print(type(posts['id']),type(id))
#                 if int(id) == posts['id']:
#                         return posts
#         return {}

# finding post from the SQL Server Postgres        




# path operation
@app.get("/")     #this decorator makes the functions work as api ,get() is the http method we used
def root():           #This function will have the code that we want to operate
    return {"message": "Welcome siddhartha bose"} #whatever we return here will be sent back to user in the website.
                                      #This return value is converted to JSON , it is the univeral language of API 

#defining above path operation
'''
get is the "HTTP Method"
root is the "function"
inside the get method is the path
''' 








