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
    post = Post(title=data["title"], content=data["content"])
    db.add(post)
    db.commit()

@app.put("/api/post/")
def editPost(data = Body(), db: Session = Depends(getDb)):
    post = db.query(Post).filter(Post.id == int(data["id"])).first()

    if post == None:
        return JSONResponse(status_code=404, content={"message": f"post with this id - {id} not found"})

    if data["title"] != "":
        post.title = data["title"]
    elif data["content"] != "":
        post.content = data["content"]
    db.commit()
    db.refresh(post)
    return post

@app.delete('/api/post/{id}')
def deletePost(id, db: Session = Depends(getDb)):
    post = db.query(Post).filter(Post.id == int(id)).first()

    if post == None:
        return JSONResponse(status_code=404, content={"message": f"post with this id - {id} not found"})

    db.delete(post)
    db.commit()
    return post


