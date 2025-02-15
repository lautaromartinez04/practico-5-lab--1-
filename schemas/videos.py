from pydantic import BaseModel

class VideoBase(BaseModel):
    video_url: str
    estado: bool
    titulo: str
    duracion: int

# Usamos Pydantic para los modelos que recibimos y enviamos
class VideoCreate(VideoBase):
    pass

class VideoResponse(VideoBase):
    id: int
    
    class Config:
        from_attributes = True
