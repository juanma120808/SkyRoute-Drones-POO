# Documento 03: Modelo del Mundo y Diagrama UML

**Proyecto:** Sistema de Gestión y Telemetría para Drones  
**Asignatura:** Algoritmos de Programación Orientada a Objetos  
**Institución:** Universidad de Medellín  

---

## Modelo del Mundo

El **Modelo del Mundo** representa las entidades abstraídas a partir del problema propuesto en el ejercicio base `ejercicio_1_poo.py`:

### Entidades y Jerarquía de Clases

1. **`TelemetriaDrone`**: Clase encargada de encapsular el estado de vuelo y lecturas de sensores de un dispositivo.
   - **Atributos:** Identificador del dron, nivel de batería, altitud actual, estado de motores y coordenadas de posición.
   - **Comportamiento:** Control de acceso mediante encapsulamiento, verificación de coherencia de estado y cálculo de distancia relativa (Haversine).

2. **Excepciones de Dominio**:
   - `TelemetriaError`: Excepción general para inconsistencias de telemetría.
   - `BateriaInvalidaError`: Excepción especializada para lecturas fuera de porcentaje permitido.
   - `AltitudInvalidaError`: Excepción especializada para lecturas fuera de límites normativos.

---

## Diagrama de Clases UML (Modelo Preliminar)

```mermaid
classDiagram
    class TelemetriaError {
    }

    class BateriaInvalidaError {
    }

    class AltitudInvalidaError {
    }

    class TelemetriaDrone {
        -_drone_id: str
        -_bateria: float
        -_altitud: float
        -_estado_motores: str
        -_coordenadas: tuple
        +validar_coherencia_estado() bool
        +calcular_distancia_haversine(destino) float
    }

    TelemetriaError <|-- BateriaInvalidaError
    TelemetriaError <|-- AltitudInvalidaError
```
