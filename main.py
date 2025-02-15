from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from fastapi.middleware.cors import CORSMiddleware
from routers.usuarios import usuarios_router
from routers.videos import videos_router  # Importa el router de videos

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos los routers
app.include_router(usuarios_router)
app.include_router(videos_router)  # Incluimos el router de videos

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')
