from sqlalchemy.orm import Session
from app.models.entities import Medico, Paciente, Cita
from app.dtos.schemas import (
    MedicoCreate, MedicoUpdate, 
    PacienteCreate, PacienteUpdate, 
    CitaCreate, CitaUpdate
)

class MedicoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Medico).all()

    def get_by_id(self, medico_id: int):
        return self.db.query(Medico).filter(Medico.id == medico_id).first()

    def get_by_doc(self, tipo: str, num: str):
        return self.db.query(Medico).filter(
            Medico.tipo_identificacion == tipo, 
            Medico.numero_identificacion == num
        ).first()

    def get_by_email(self, correo: str):
        return self.db.query(Medico).filter(Medico.correo == correo).first()

    def create(self, medico: MedicoCreate):
        db_medico = Medico(**medico.model_dump())
        self.db.add(db_medico)
        self.db.commit()
        self.db.refresh(db_medico)
        return db_medico

    def update(self, medico_id: int, data: MedicoUpdate):
        db_medico = self.get_by_id(medico_id)
        if db_medico:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(db_medico, key, value)
            self.db.commit()
            self.db.refresh(db_medico)
        return db_medico


class PacienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Paciente).all()

    def get_by_id(self, paciente_id: int):
        return self.db.query(Paciente).filter(Paciente.id == paciente_id).first()

    def get_by_doc(self, tipo: str, num: str):
        return self.db.query(Paciente).filter(
            Paciente.tipo_identificacion == tipo, 
            Paciente.numero_identificacion == num
        ).first()

    def get_by_email(self, correo: str):
        return self.db.query(Paciente).filter(Paciente.correo == correo).first()

    def create(self, paciente: PacienteCreate):
        db_paciente = Paciente(**paciente.model_dump())
        self.db.add(db_paciente)
        self.db.commit()
        self.db.refresh(db_paciente)
        return db_paciente

    def update(self, paciente_id: int, data: PacienteUpdate):
        db_paciente = self.get_by_id(paciente_id)
        if db_paciente:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(db_paciente, key, value)
            self.db.commit()
            self.db.refresh(db_paciente)
        return db_paciente


class CitaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Cita).all()

    def get_by_id(self, cita_id: int):
        return self.db.query(Cita).filter(Cita.id == cita_id).first()

    def get_by_medico_fecha_hora(self, medico_id: int, fecha, hora):
        return self.db.query(Cita).filter(
            Cita.medico_id == medico_id,
            Cita.fecha == fecha,
            Cita.hora == hora
        ).first()

    def create(self, cita: CitaCreate):
        db_cita = Cita(**cita.model_dump())
        self.db.add(db_cita)
        self.db.commit()
        self.db.refresh(db_cita)
        return db_cita

    def update(self, cita_id: int, data: CitaUpdate):
        db_cita = self.get_by_id(cita_id)
        if db_cita:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(db_cita, key, value)
            self.db.commit()
            self.db.refresh(db_cita)
        return db_cita