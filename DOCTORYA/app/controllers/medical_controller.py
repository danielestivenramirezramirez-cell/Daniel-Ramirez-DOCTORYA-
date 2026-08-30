from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.dtos.schemas import (
    MedicoCreate, MedicoUpdate, MedicoResponse,
    PacienteCreate, PacienteUpdate, PacienteResponse,
    CitaCreate, CitaUpdate, CitaResponse
)
from app.services.medical_service import MedicoService, PacienteService, CitaService
from app.patterns.appointment_strategy import (
    GeneralConsultationStrategy, 
    SpecialistConsultationStrategy, 
    EmergencyConsultationStrategy
)
from app.patterns.notification_factory import NotificationFactory
from app.patterns.payment_adapter import ExternalPaymentGateway, PaymentAdapter

router = APIRouter()

# ================= RUTAS MÉDICOS =================

@router.get("/medicos", response_model=List[MedicoResponse], tags=["Médicos"])
def get_medicos(db: Session = Depends(get_db)):
    return MedicoService(db).listar_medicos()

@router.get("/medicos/buscar-por-identificacion", response_model=MedicoResponse, tags=["Médicos"])
def get_medico_por_identificacion(tipo_doc: str, num_doc: str, db: Session = Depends(get_db)):
    medico = MedicoService(db).obtener_por_identificacion(tipo_doc, num_doc)
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return medico

@router.get("/medicos/buscar-por-correo", response_model=MedicoResponse, tags=["Médicos"])
def get_medico_por_correo(correo: str, db: Session = Depends(get_db)):
    medico = MedicoService(db).obtener_por_correo(correo)
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return medico

@router.post("/medicos", response_model=MedicoResponse, status_code=status.HTTP_201_CREATED, tags=["Médicos"])
def create_medico(data: MedicoCreate, db: Session = Depends(get_db)):
    return MedicoService(db).registrar_medico(data)

@router.put("/medicos/{medico_id}", response_model=MedicoResponse, tags=["Médicos"])
def update_medico(medico_id: int, data: MedicoUpdate, db: Session = Depends(get_db)):
    return MedicoService(db).actualizar_medico(medico_id, data)


# ================= RUTAS PACIENTES =================

@router.get("/pacientes", response_model=List[PacienteResponse], tags=["Pacientes"])
def get_pacientes(db: Session = Depends(get_db)):
    return PacienteService(db).listar_pacientes()

@router.get("/pacientes/buscar-por-identificacion", response_model=PacienteResponse, tags=["Pacientes"])
def get_paciente_por_identificacion(tipo_doc: str, num_doc: str, db: Session = Depends(get_db)):
    paciente = PacienteService(db).obtener_por_identificacion(tipo_doc, num_doc)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@router.get("/pacientes/buscar-por-correo", response_model=PacienteResponse, tags=["Pacientes"])
def get_paciente_por_correo(correo: str, db: Session = Depends(get_db)):
    paciente = PacienteService(db).obtener_por_correo(correo)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@router.post("/pacientes", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED, tags=["Pacientes"])
def create_paciente(data: PacienteCreate, db: Session = Depends(get_db)):
    return PacienteService(db).registrar_paciente(data)

@router.put("/pacientes/{paciente_id}", response_model=PacienteResponse, tags=["Pacientes"])
def update_paciente(paciente_id: int, data: PacienteUpdate, db: Session = Depends(get_db)):
    return PacienteService(db).actualizar_paciente(paciente_id, data)


# ================= RUTAS CITAS =================

@router.get("/citas", response_model=List[CitaResponse], tags=["Citas"])
def get_citas(db: Session = Depends(get_db)):
    return CitaService(db).listar_citas()

@router.get("/citas/{cita_id}", response_model=CitaResponse, tags=["Citas"])
def get_cita_por_id(cita_id: int, db: Session = Depends(get_db)):
    cita = CitaService(db).obtener_por_id(cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

@router.post("/citas", response_model=CitaResponse, status_code=status.HTTP_201_CREATED, tags=["Citas"])
def create_cita(data: CitaCreate, db: Session = Depends(get_db)):
    return CitaService(db).agendar_cita(data)

@router.put("/citas/{cita_id}", response_model=CitaResponse, tags=["Citas"])
def update_cita(cita_id: int, data: CitaUpdate, db: Session = Depends(get_db)):
    return CitaService(db).actualizar_cita(cita_id, data)


# ================= RUTAS PATRONES DE DISEÑO =================

@router.get("/patterns/calcular-precio/", tags=["Patrones de Diseño"])
def calcular_precio_cita(tipo: str, precio_base: float = 50000.0):
    tipo_clean = tipo.lower()
    if tipo_clean == "general":
        strategy = GeneralConsultationStrategy()
    elif tipo_clean == "especialista":
        strategy = SpecialistConsultationStrategy()
    elif tipo_clean == "urgencia":
        strategy = EmergencyConsultationStrategy()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Tipo de consulta no válido. Use 'general', 'especialista' o 'urgencia'."
        )
    
    total = strategy.calculate_price(precio_base)
    return {"tipo_consulta": tipo_clean, "precio_base": precio_base, "total": total}


@router.post("/patterns/enviar-notificacion/", tags=["Patrones de Diseño"])
def enviar_notificacion(tipo: str, destinatario: str, mensaje: str):
    try:
        notifier = NotificationFactory.get_notifier(tipo)
        resultado = notifier.send(mensaje, destinatario)
        return {"status": "exitoso", "detalle": resultado}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/patterns/procesar-pago/", tags=["Patrones de Diseño"])
def procesar_pago(correo: str, monto: float):
    gateway_externo = ExternalPaymentGateway()
    adaptador = PaymentAdapter(gateway_externo)
    resultado = adaptador.pay(monto, correo)
    return {"status": "exitoso", "respuesta": resultado}