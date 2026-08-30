from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo_identificacion = Column(String, nullable=False)
    numero_identificacion = Column(String, unique=True, nullable=False)
    especialidad = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)

    citas = relationship("Cita", back_populates="medico")


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo_identificacion = Column(String, nullable=False)
    numero_identificacion = Column(String, unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    telefono = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)

    citas = relationship("Cita", back_populates="paciente")


class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    motivo = Column(String, nullable=False)
    estado = Column(String, default="Programada")

    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)

    medico = relationship("Medico", back_populates="citas")
    paciente = relationship("Paciente", back_populates="citas")