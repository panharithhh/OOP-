from sqlalchemy import Column, Integer, String
from .database import Base  # It defines how your application data is struturedjj

class Blog(Base): # this make when the data is save it wil recognize the type of data
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)