from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    photos = relationship("Photo", back_populates="owner", cascade="all, delete")
    videos = relationship("Video", back_populates="owner", cascade="all, delete")
    etkinlikler = relationship("Etkinlik", back_populates="kullanici", cascade="all, delete")


class Etkinlik(Base):
    __tablename__ = "etkinlikler"

    id = Column(Integer, primary_key=True, index=True)
    etkinlik_adi = Column(String, nullable=False)
    kullanici_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tarih = Column(DateTime, default=datetime.utcnow)
    anahtar_kelime = Column(String, nullable=True)
    qr_kodu = Column(String, nullable=True)
    misafir_sayisi = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    # İlişkiler
    resimler = relationship("Photo", back_populates="etkinlik", cascade="all, delete")
    videolar = relationship("Video", back_populates="etkinlik", cascade="all, delete")
    kullanici = relationship("User", back_populates="etkinlikler")

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)  # yeni alan
    etkinlik_id = Column(Integer, ForeignKey("etkinlikler.id"))
    owner = relationship("User", back_populates="photos")
    etkinlik = relationship("Etkinlik", back_populates="resimler")

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow) 
    etkinlik_id = Column(Integer, ForeignKey("etkinlikler.id"))
    owner = relationship("User", back_populates="videos")   
    etkinlik = relationship("Etkinlik", back_populates="videolar")