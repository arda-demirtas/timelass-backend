from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class PhotoBase(BaseModel):
    url: str
    etkinlik_id: int
    created_at: datetime

class PhotoCreate(PhotoBase):
    pass

class Photo(PhotoBase):
    id: int
    class Config:
        orm_mode = True


class VideoBase(BaseModel):
    url: str
    etkinlik_id: int
    created_at: datetime

class VideoCreate(VideoBase):
    pass

class Video(VideoBase):
    id: int
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class EtkinlikBase(BaseModel):
    etkinlik_adi: str
    tarih: Optional[datetime] = None
    anahtar_kelime: Optional[str] = None
    qr_kodu: Optional[str] = None
    

class EtkinlikCreate(EtkinlikBase):
    kullanici_id: int
    location : str

    

class EtkinlikUpdate(EtkinlikBase):
    location : str
    resimler: List[Photo]
    videolar : List[Video]

class EtkinlikInDB(EtkinlikBase):
    id: int
    kullanici_id: int
    resimler: List[Photo] = []
    videolar: List[Video] = []
    misafir_sayisi: Optional[int] = 0
    class Config:
        orm_mode = True

        
class User(UserBase):
    id: int
    password : str
    photos: List[Photo] = []
    videos: List[Video] = []
    etkinlikler : List[EtkinlikInDB] = []
    class Config:
        orm_mode = True

class PhotoCreate(BaseModel):
    url: str
    user_id: int
    etkinlik_id: int

class VideoCreate(BaseModel):
    url: str
    user_id: int
    etkinlik_id: int