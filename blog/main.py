from . import model, schemas
from typing import List 
from .database import engine, SessionLocal
from fastapi import FastAPI, Depends, status , Response , HTTPException
from sqlalchemy.orm import Session
from . import schemas, model
from passlib.context import CryptContext

import logging

# # Configure logging (optional but recommended)
# logging.basicConfig(level=logging.ERROR)
# logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()  # Create a session instance here
    try:
        yield db
    finally:
        db.close()  # Close the session, not the sessionmaker


app = FastAPI()
model.Base.metadata.create_all(bind=engine)


@app.post('/blog', status_code= status.HTTP_201_CREATED, tags = ['blog'])
def create(request: schemas.Blog, db: Session = Depends(get_db)): 
        new_blog = model.Blog(title=request.title, body=request.body)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
   
    

@app.get('/blog' ,response_model = List[schemas.ShowBlog], tags = ['blog'])
def all(db : Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code= 200, response_model= schemas.ShowBlog, tags = ['blog'])
def show(id , reponse : Response , db : Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    
    if not blog:
        
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"the {id} id doesn't exit")
        
        #response.status_code = status.http..
        # return {'detail' : f:Blog is no .. }
     
    return blog

# @app.delete('/blog/{title}', status_code=status.HTTP_204_NO_CONTENT)
# def destroy_by_title(title: str, db: Session = Depends(get_db)):
#     db.query(model.Blog).filter(model.Blog.title == title).delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete('/blog/{id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['blog'])
def destroy(id, db : Session = Depends(get_db)):
    db.query(model.Blog).filter(model.Blog.id == id).delete(synchronize_session= False)
    db.commit()
    return 'done'
    
    
    
@app.put('/blog/{id}' , status_code= status.HTTP_202_ACCEPTED , tags = ['blog'])
def update(id , request: schemas.Blog, db : Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    if not blog.first(): 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"blog {id} don;t exist")
    
    update_data = request.model_dump(exclude_unset=True) # Convert to dict
    blog.update(update_data, synchronize_session=False) # Pass the dict    
    db.commit()
    return 'updated'

pwd_cxt  =  CryptContext(schemes=["bcrypt"], deprecated = " auto" )

@app.post('/user', response_model = schemas.ShowUser , tags = ['user']  )

def create_user(request : schemas.User , db : Session = Depends(get_db)):
    hashedpassword = pwd_cxt.hash(request.password)
    new_user = model.User(name = request.name, email = request.email, password = hashedpassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    return request

@app.get('/user/{id}', response_model = schemas.ShowUser, tags = ['user'])
def show_user(id,db : Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"blog {id} don;t exist")
    return user
        
@app.get('/user', tags = ['user'])
def all_user(db : Session = Depends(get_db)):           
    blogs = db.query(model.User).all()
    return blogs 

       