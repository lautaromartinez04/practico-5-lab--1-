from sqlalchemy import Column, Integer, String, Boolean
from config.database import Base

# Modelo para la tabla de videos
class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    video_url = Column(String(255), index=True)
    estado = Column(Boolean, default=True)
    titulo = Column(String(255), index=True)
    duracion = Column(Integer)  # Duración en segundos
