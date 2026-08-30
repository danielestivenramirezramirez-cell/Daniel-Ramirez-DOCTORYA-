from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_pattern_strategy():
    response = client.get(
        "/api/v1/patterns/calcular-precio/",
        params={"tipo": "especialista", "precio_base": 100000}
    )
    assert response.status_code == 200
    assert response.json()["total"] == 150000.0

def test_pattern_factory():
    response = client.post(
        "/api/v1/patterns/enviar-notificacion/",
        params={"tipo": "email", "destinatario": "test@correo.com", "mensaje": "Hola"}
    )
    assert response.status_code == 200
    assert "Enviando Email" in response.json()["detalle"]

def test_pattern_adapter():
    response = client.post(
        "/api/v1/patterns/procesar-pago/",
        params={"correo": "test@correo.com", "monto": 50000}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "exitoso"