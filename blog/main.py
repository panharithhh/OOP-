from . import model, schemas
from .database import engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, model
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


@app.post('/blog')
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    try: 
        new_blog = model.Blog(title=request.title, body=request.body)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except Exception as e:
        logger.error(f"Error creating blog post: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")