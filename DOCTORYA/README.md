# DOCTORYA - Sistema de Gestión de Citas Médicas

API REST desarrollada con **FastAPI**, **Python** y **PostgreSQL** para la gestión de médicos, pacientes y citas médicas en el sistema DOCTORYA.

- **Despliegue en producción:** [DOCTORYA API Documentation](https://daniel-ramirez-doctorya.onrender.com/docs)
- **Repositorio oficial:** [GitHub - Daniel-Ramirez-DOCTORYA](https://github.com/danielestivenramirezramirez-cell/Daniel-Ramirez-DOCTORYA-)

---

## 🏛️ Arquitectura por Capas

El proyecto implementa una arquitectura desacoplada por capas:

```text
Actor -> Controlador -> Servicio -> Repositorio -> PostgreSQL