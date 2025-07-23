from database import *
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

def getDb():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return FileResponse("public/index.html")

@app.get("/api/posts")
def getAllPOsts(db: Session = Depends(getDb)):
    return db.query(Post).all()

@app.get("/api/posts/{id}")
def getParticularPost(id, db: Session = Depends(getDb)):
    posts = db.query(Post).all()
    for post in posts:
        if post.id == int(id):
            return post

@app.post("/api/posts")
def createPost(data = Body(), db: Session = Depends(getDb)):
    post = Post(title=data["title"], content=data["content"])
    db.add(post)
    db.commit()



