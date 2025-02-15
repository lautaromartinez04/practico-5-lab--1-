import os
from moviepy import VideoFileClip
from sqlalchemy.orm import Session
from models.videos import Video
from schemas.videos import VideoCreate
from pathlib import Path

# Carpeta donde se almacenarán los videos
UPLOAD_FOLDER = "./videos/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_video(file, video_id) -> str:
    # Crear un nombre de archivo único basado en el ID del video
    unique_name = f"video{video_id}.mp4"
    file_location = os.path.join(UPLOAD_FOLDER, unique_name)
    
    # Guardar el archivo con el nombre basado en el ID
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())
    
    return file_location

def obtener_duracion(video_path: str) -> int:
    try:
        video = VideoFileClip(video_path)
        return int(video.duration)  # Duración en segundos
    except Exception as e:
        return 0

def crear_video(db: Session, file) -> Video:
    # Crear un nuevo registro en la base de datos (sin archivo aún)
    titulo = Path(file.filename).stem
    db_video = Video(
        video_url="",  # El campo de video_url está vacío por ahora
        estado=True,
        titulo=titulo,
        duracion=0  # La duración se calculará después
    )
    
    db.add(db_video)
    db.commit()
    db.refresh(db_video)  # Obtén el ID recién generado

    # Guardar el archivo con el nombre basado en el ID del video
    video_path = save_video(file, db_video.id)
    
    # Obtener la duración del video
    duracion = obtener_duracion(video_path)
    
    # Actualizar la URL y la duración en la base de datos
    db_video.video_url = video_path
    db_video.duracion = duracion
    
    db.commit()  # Guardamos los cambios en la base de datos
    
    return db_video

def obtener_videos(db: Session) -> list[Video]:
    videos = db.query(Video).all()
    return videos

def borrrar_video(db: Session, video_id: int) -> None:
    db.query(Video).filter(Video.id == video_id).delete()
    db.commit()
    os.remove(f"./videos/video{video_id}.mp4")
    return  

def cambiar_estado(db: Session, video_id: int) -> None:
    # Obtener el video con el id especificado
    video = db.query(Video).filter(Video.id == video_id).first()

    # Si el video existe, cambiar el estado
    if video:
        video.estado = not video.estado  # Cambiar el estado de True a False o viceversa
        db.commit()
    else:
        print(f"El video con ID {video_id} no existe.")
