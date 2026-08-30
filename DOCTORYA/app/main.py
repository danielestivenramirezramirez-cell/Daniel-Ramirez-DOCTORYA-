from fastapi import FastAPI
from app.config.database import engine, Base
from app.controllers.medical_controller import router as medical_router

# Crea las tablas en la base de datos automáticamente si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DOCTORYA API",
    description="API RESTful para la gestión de médicos, pacientes y citas médicas",
    version="1.0.0"
)

# Incluir las rutas del controlador
app.include_router(medical_router, prefix="/api/v1", tags=["Sistema Médico"])

@app.get("/", tags=["Inicio"])
def root():
    return {"message": "Bienvenido a la API de DOCTORYA"}

@app.get("/health", tags=["Salud"])
def health_check():
    return {
        "status": "ok",
        "service": "DOCTORYA API",
        "version": "1.0.0"
    }
    