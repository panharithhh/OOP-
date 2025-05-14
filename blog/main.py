from . import model, schemas
from .database import engine, SessionLocal
from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from . import schemas, model

def get_db(): 
    db = SessionLocal
    try: 
        yield db
    finally : 
        db.close
    
app = FastAPI()
model.Base.metadata.create_all(bind=engine)

@app.post('blog')
def create(request: schemas.Blog, db : Session = Depends(get_db)):
    return db



