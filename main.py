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
def getAllPosts(db: Session = Depends(getDb)):
    #done
    return db.query(Post).all()

@app.get("/api/posts/{id}")
def getParticularPost(id, db: Session = Depends(getDb)):
    post = db.query(Post).filter(Post.id == int(id)).first()
    if post == None:
        return JSONResponse(status_code=404, content={"message": "Пост с таким id не найден"})
    else:
        return post

@app.post("/api/posts")
def createPost(data = Body(), db: Session = Depends(getDb)):
    #done
    post = Post(title=data["title"], content=data["content"])
    db.add(post)
    db.commit()

@app.put("/api/posts")
def editPost(data = Body(), db: Session = Depends(getDb)):
    post = db.query(Post).filter(Post.id == data["id"]).first()
    if post == None:
        return JSONResponse(status_code=404, content={"message": "Пост с таким id не найден"})
    else:
        return post



