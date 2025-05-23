from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import desc
from database import SessionLocal, engine, Base
import models, schemas, crud
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)
from datetime import datetime

origins = [
"*"  # Alternatif local host
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # React frontend'in URL'si
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE vs. izin ver
    allow_headers=["*"],
)
# DB session dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Kullanıcı oluştur
@app.get("/")
def dddd():
    return {"message" : "basarili2"}
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return db_user

# Kullanıcıyı ID ile getir
@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Fotoğraf ekle
@app.post("/users/{user_id}/photos/", response_model=schemas.Photo)
def add_photo(user_id: int, photo: schemas.PhotoCreate, db: Session = Depends(get_db)):
    return crud.create_photo(db, user_id, photo)

# Video ekle
@app.post("/users/{user_id}/videos/", response_model=schemas.Video)
def add_video(user_id: int, video: schemas.VideoCreate, db: Session = Depends(get_db)):
    return crud.create_video(db, user_id, video)

# Tüm kullanıcılar (opsiyonel)
@app.get("/users/", response_model=List[schemas.User])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

def get_user_photos_paginated(db: Session, user_id: int, offset: int = 0, limit: int = 10):
    return (
        db.query(models.Photo)
        .filter(models.Photo.user_id == user_id)
        .order_by(desc(models.Photo.created_at))
        .offset(offset)
        .limit(limit)
        .all()
    )
@app.get("/users/{user_id}/photos", response_model=List[schemas.Photo])
def get_photos_paginated(
    user_id: int,
    db: Session = Depends(get_db),
    page: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    
):
    offset = page * limit
    print("OFFSET:", offset)
    return get_user_photos_paginated(db, user_id, offset=offset, limit=limit)


@app.get("/users/{user_id}/videos", response_model=List[schemas.Video])
def get_user_videos_paginated(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Video)
        .filter(models.Video.user_id == user_id)
        .order_by(desc(models.Video.created_at))  # en yeni önce
        .offset(skip)
        .limit(limit)
        .all()
    )
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password

@app.post("/users/login")
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_login.email).first()
    if not user or not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "user": {
            
            "id": user.id,
            "email": user.email,
            "username" : user.username
        }
    }


@app.post("/etkinlik", response_model=schemas.EtkinlikInDB)
def create_new_etkinlik(etkinlik: schemas.EtkinlikCreate, db: Session = Depends(get_db)):
    try:
        print(etkinlik)
        xd = crud.create_etkinlik(db, etkinlik)
        return xd
    except Exception as e:
        print("Hata:", e)
        traceback.print_exc()  # stack trace yazdır
        raise


@app.get("/etkinlik/{etkinlik_id}", response_model=schemas.EtkinlikInDB)
def read_etkinlik(etkinlik_id: int, db: Session = Depends(get_db)):
    db_etkinlik = crud.get_etkinlik(db, etkinlik_id)
    if not db_etkinlik:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")
    return db_etkinlik

@app.get("/user/etkinlik/{kullanici_id}", response_model=list[schemas.EtkinlikInDB])
def read_etkinlikler_by_user(
    kullanici_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_etkinlikler_by_user(db, kullanici_id, skip=skip, limit=limit)

@app.put("/etkinlik/{etkinlik_id}", response_model=schemas.EtkinlikInDB)
def update_existing_etkinlik(etkinlik_id: int, etkinlik_update: schemas.EtkinlikUpdate, db: Session = Depends(get_db)):
    updated = crud.update_etkinlik(db, etkinlik_id, etkinlik_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")
    return updated

@app.delete("/etkinlik/{etkinlik_id}", response_model=schemas.EtkinlikInDB)
def delete_etkinlik_endpoint(etkinlik_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_etkinlik(db, etkinlik_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")
    return deleted


@app.post("/photos/", status_code=201)
def add_photo(photo: schemas.PhotoCreate, db: Session = Depends(get_db)):
    etkinlik = db.query(models.Etkinlik).filter(models.Etkinlik.id == photo.etkinlik_id).first()
    if not etkinlik:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı.")

    new_photo = models.Photo(
        url=photo.url,
        user_id=photo.user_id,
        etkinlik_id=photo.etkinlik_id,
        created_at=datetime.utcnow()
    )
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return {"message": "Fotoğraf eklendi", "photo_id": new_photo.id}

# -------------------------------
# 🎥 Video Ekleme Endpoint’i
# -------------------------------

@app.post("/videos/", status_code=201)
def add_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    etkinlik = db.query(models.Etkinlik).filter(models.Etkinlik.id == video.etkinlik_id).first()
    if not etkinlik:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı.")

    new_video = models.Video(
        url=video.url,
        user_id=video.user_id,
        etkinlik_id=video.etkinlik_id,
        created_at=datetime.utcnow()
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return {"message": "Video eklendi", "video_id": new_video.id}
