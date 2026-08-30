from fastapi import HTTPException, status
from app.repositories.medical_repository import MedicoRepository, PacienteRepository, CitaRepository
from app.dtos.schemas import (
    MedicoCreate, MedicoUpdate, 
    PacienteCreate, PacienteUpdate, 
    CitaCreate, CitaUpdate
)

class MedicoService:
    def __init__(self, repo: MedicoRepository):
        self.repo = repo

    def obtener_todos(self):
        return self.repo.get_all()

    def obtener_por_documento(self, tipo: str, num: str):
        medico = self.repo.get_by_doc(tipo, num)
        if not medico:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado.")
        return medico

    def obtener_por_correo(self, correo: str):
        medico = self.repo.get_by_email(correo)
        if not medico:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado.")
        return medico

    def crear(self, data: MedicoCreate):
        if self.repo.get_by_doc(data.tipo_identificacion, data.numero_identificacion):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un médico con esta identificación.")
        if self.repo.get_by_email(data.correo):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un médico con este correo.")
        return self.repo.create(data)

    def actualizar(self, medico_id: int, data: MedicoUpdate):
        medico = self.repo.update(medico_id, data)
        if not medico:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado.")
        return medico


class PacienteService:
    def __init__(self, repo: PacienteRepository):
        self.repo = repo

    def obtener_todos(self):
        return self.repo.get_all()

    def obtener_por_documento(self, tipo: str, num: str):
        paciente = self.repo.get_by_doc(tipo, num)
        if not paciente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado.")
        return paciente

    def obtener_por_correo(self, correo: str):
        paciente = self.repo.get_by_email(correo)
        if not paciente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado.")
        return paciente

    def crear(self, data: PacienteCreate):
        if self.repo.get_by_doc(data.tipo_identificacion, data.numero_identificacion):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un paciente con esta identificación.")
        if self.repo.get_by_email(data.correo):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un paciente con este correo.")
        return self.repo.create(data)

    def actualizar(self, paciente_id: int, data: PacienteUpdate):
        paciente = self.repo.update(paciente_id, data)
        if not paciente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado.")
        return paciente


class CitaService:
    def __init__(self, cita_repo: CitaRepository, medico_repo: MedicoRepository, paciente_repo: PacienteRepository):
        self.cita_repo = cita_repo
        self.medico_repo = medico_repo
        self.paciente_repo = paciente_repo

    def obtener_todas(self):
        return self.cita_repo.get_all()

    def obtener_por_id(self, cita_id: int):
        cita = self.cita_repo.get_by_id(cita_id)
        if not cita:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada.")
        return cita

    def crear(self, data: CitaCreate):
        # 1. Validar existencia del médico por ID utilizando la sesión del repositorio
        medico = self.medico_repo.db.query(self.medico_repo.db.models.entities.Medico).filter_by(id=data.medico_id).first() if hasattr(self.medico_repo.db, 'models') else None
        if not medico:
            # Fallback simple si la entidad no está mapeada dinámicamente en db
            medicos = self.medico_repo.get_all()
            if not any(m.id == data.medico_id for m in medicos):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El médico especificado no existe.")

        # 2. Validar existencia del paciente por ID
        pacientes = self.paciente_repo.get_all()
        if not any(p.id == data.paciente_id for p in pacientes):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El paciente especificado no existe.")

        # 3. Validar cruce de horario del médico
        cita_existente = self.cita_repo.get_by_medico_fecha_hora(data.medico_id, data.fecha, data.hora)
        if cita_existente:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El médico ya tiene una cita programada en la misma fecha y hora.")

        return self.cita_repo.create(data)

    def actualizar(self, cita_id: int, data: CitaUpdate):
        cita = self.cita_repo.update(cita_id, data)
        if not cita:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada.")
        return cita