from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from services.videos import crear_video, obtener_videos, borrrar_video, cambiar_estado
from schemas.videos import VideoResponse
from config.database import Session

videos_router = APIRouter()

# Función para obtener la sesión de la base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@videos_router.get("/videos", response_model=list[VideoResponse], status_code=200, tags=["Videos"])   
async def get_videos(db: Session = Depends(get_db)):
    # Usamos el servicio para obtener los videos
    videos = obtener_videos(db)
    return videos


# Endpoint para subir el video
@videos_router.post("/upload_video/", response_model=VideoResponse, status_code=201, tags=["Videos"])
async def upload_video(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Usamos el servicio para crear el video
    db_video = crear_video(db, file)
    return db_video

@videos_router.delete("/videos/{id}", response_model=dict, status_code=200, tags=["Videos"])
async def delete_video(id: int, db: Session = Depends(get_db)):
    # Usamos el servicio para borrar el video    
    borrrar_video(db, id)
    return {"message": "Video borrado"}

@videos_router.put("/videos/{id}/estado", response_model=dict, status_code=200, tags=["Videos"])
async def cambiar_estado_video(id: int, db: Session = Depends(get_db)):
    # Usamos el servicio para cambiar el estado del video
    cambiar_estado(db, id)
    return {"message": "Estado del video cambiado"}