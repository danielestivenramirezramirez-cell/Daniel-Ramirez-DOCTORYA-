from pydantic import BaseModel, EmailStr
from datetime import date, time
from typing import Optional

# --- DTOs MÉRICO ---
class MedicoBase(BaseModel):
    nombre: str
    tipo_identificacion: str
    numero_identificacion: str
    especialidad: str
    telefono: str
    correo: EmailStr

class MedicoCreate(MedicoBase):
    pass

class MedicoUpdate(BaseModel):
    nombre: Optional[str] = None
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None

class MedicoResponse(MedicoBase):
    id: int
    class Config:
        from_attributes = True

# --- DTOs PACIENTE ---
class PacienteBase(BaseModel):
    nombre: str
    tipo_identificacion: str
    numero_identificacion: str
    fecha_nacimiento: date
    telefono: str
    correo: EmailStr

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None

class PacienteResponse(PacienteBase):
    id: int
    class Config:
        from_attributes = True

# --- DTOs CITA ---
class CitaBase(BaseModel):
    fecha: date
    hora: time
    motivo: str
    medico_id: int
    paciente_id: int

class CitaCreate(CitaBase):
    pass

class CitaUpdate(BaseModel):
    fecha: Optional[date] = None
    hora: Optional[time] = None
    motivo: Optional[str] = None
    estado: Optional[str] = None

class CitaResponse(CitaBase):
    id: int
    estado: str
    medico: MedicoResponse
    paciente: PacienteResponse
    class Config:
        from_attributes = True