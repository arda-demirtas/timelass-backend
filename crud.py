from sqlalchemy.orm import Session
import models
import schemas

# Kullanıcı oluştur
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Tüm kullanıcıları getir
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Kullanıcı ID ile getir
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Foto ekle
def create_photo(db: Session, user_id: int, photo: schemas.PhotoCreate):
    db_photo = models.Photo(**photo.dict(), user_id=user_id)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

# Video ekle
def create_video(db: Session, user_id: int, video: schemas.VideoCreate):
    db_video = models.Video(**video.dict(), user_id=user_id)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def get_user_photos_paginated(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Photo).filter(models.Photo.user_id == user_id).offset(skip).limit(limit).all()




def create_etkinlik(db: Session, etkinlik: schemas.EtkinlikCreate):
    db_etkinlik = models.Etkinlik(
        etkinlik_adi=etkinlik.etkinlik_adi,
        kullanici_id=etkinlik.kullanici_id,
        tarih=etkinlik.tarih,
        anahtar_kelime=etkinlik.anahtar_kelime,
        qr_kodu=etkinlik.qr_kodu,
        misafir_sayisi = 0
    )
    db.add(db_etkinlik)
    db.commit()
    db.refresh(db_etkinlik)
    return db_etkinlik

def get_etkinlik(db: Session, etkinlik_id: int):
    return db.query(models.Etkinlik).filter(models.Etkinlik.id == etkinlik_id).first()

def get_etkinlikler_by_user(db: Session, kullanici_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Etkinlik)
        .filter(models.Etkinlik.kullanici_id == kullanici_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def update_etkinlik(db: Session, etkinlik_id: int, etkinlik_update: schemas.EtkinlikUpdate):
    db_etkinlik = get_etkinlik(db, etkinlik_id)
    if not db_etkinlik:
        return None
    for key, value in etkinlik_update.dict(exclude_unset=True).items():
        setattr(db_etkinlik, key, value)
    db.commit()
    db.refresh(db_etkinlik)
    return db_etkinlik

def delete_etkinlik(db: Session, etkinlik_id: int):
    db_etkinlik = get_etkinlik(db, etkinlik_id)
    if not db_etkinlik:
        return None
    db.delete(db_etkinlik)
    db.commit()
    return db_etkinlik