# Documento 01: Descripción e Historial del Problema

**Proyecto:** SkyRoute - Sistema de Gestión y Telemetría para Drones  
**Asignatura:** Algoritmos de Programación Orientada a Objetos  
**Institución:** Universidad de Medellín (UDEM)  
**Semestre:** 2026-2  
**Docente:** Mario Alejandro Saldarriaga (Grupo 62)  
**Equipo:** Alejandro García Jiménez, Juan Manuel Pava Higuita, Valery Arboleda Ardila  

---

## 1. Contexto del Problema

Una empresa dedicada al transporte y logística mediante aeronaves no tripuladas (drones) para entregas de última milla requiere un módulo de software de alta confiabilidad capaz de recibir, procesar y validar tramas de telemetría emitidas en tiempo real por los sensores a bordo.

En operaciones aeronáuticas civiles y logísticas, la integridad de los datos reportados es crítica para la seguridad del espacio aéreo. El módulo **SkyRoute Telemetry Core** opera como la primera línea de defensa antes de transmitir la información al centro de control de tráfico aéreo. Su misión es detectar y rechazar inmediatamente tramas corruptas, fuera de norma legal o físicamente contradictorias (como altitudes superiores al techo permitido o motores apagados cuando el dron se encuentra a gran altura).

---

## 2. Historial de Desarrollo y Arquitectura Incremental

1. **Fase 1 - Core de Dominio y Validaciones:** Implementación inicial de la entidad de telemetría (`src/telemetria.py`), jerarquía de excepciones (`src/exceptions.py`) y cálculo geodésico de Haversine (`src/utils/geodesia.py`).
2. **Fase 2 - Blindaje de Invariantes y Tipos:**
   - **Validación cruzada bidireccional:** Garantiza que la coherencia entre altitud y estado de motores se preserve tanto en la instanciación inicial como en mutaciones posteriores (`altitud > 0` $\iff$ `motores == EN_VUELO`).
   - **Exclusión estricta de booleanos:** Previene que valores `bool` pasen como números válidos en las propiedades de negocio.
3. **Fase 3 - Análisis Formal y Modelo del Mundo (Entregable 1):** Consolidación metodológica conforme a la rúbrica oficial de la UDEM:
   - Requisitos Funcionales normalizados (R1, R2, R3, R4).
   - Reglas de Negocio claras e inequívocas.
   - Comprensión del Mundo del Problema y Asignación de Responsabilidades.
   - Diagrama de Clases UML en Mermaid con relaciones de herencia y dependencia.
   - Suite de 20 pruebas unitarias automatizadas (`tests/`).
