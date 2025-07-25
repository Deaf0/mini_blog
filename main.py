from database import *
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Union
from schemas import PostCreate, PostEdit, PostResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return FileResponse("public/index.html")

@app.get("/api/posts", response_model=List[PostResponse])
def getAllPosts(db: Session = Depends(getDb)):
    return db.query(Post).all()

@app.get("/api/posts/{id}", response_model=PostResponse)
def getParticularPost(id: int, db: Session = Depends(getDb)):
    post = db.query(Post).filter(Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return post

@app.post("/api/posts", status_code=201, response_model=PostResponse)
def createPost(data: PostCreate, db: Session = Depends(getDb)):
    post = Post(title=data.title, content=data.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.put("/api/post/{id}", response_model=PostResponse)
def editPost(id: int, data: PostEdit, db: Session = Depends(getDb)):
    post = db.query(Post).filter(Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=404, detail="Post not found")

    if data.title:
        post.title = data.title
    if data.content:
        post.content = data.content
    db.commit()
    db.refresh(post)
    return post

@app.delete('/api/post/{id}', status_code=200, response_model=PostResponse)
def deletePost(id: int, db: Session = Depends(getDb)):
    post = db.query(Post).filter(Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return post


