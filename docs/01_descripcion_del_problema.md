# Documento 01: Descripción e Historial del Problema

**Proyecto:** SkyRoute - Sistema de Gestión y Telemetría para Drones  
**Asignatura:** Algoritmos de Programación Orientada a Objetos  
**Institución:** Universidad de Medellín (UDEM)  
**Semestre:** 2026-2  

---

## 1. Contexto del Problema

Una empresa dedicada al transporte y logística mediante aeronaves no tripuladas (drones) requiere un módulo de software capaz de recibir, procesar y validar tramas de telemetría en tiempo real.

En operaciones aeronáuticas, la integridad de los datos recibidos de los sensores es fundamental. El software debe actuar como una capa de validación previa que identifique e impida el procesamiento de tramas con datos inconsistentes o fuera de los rangos operacionales permitidos (como niveles inválidos de batería, altitudes fuera de norma o incoherencias entre el estado de los motores y la altitud del dispositivo).

---

## 2. Historial de Desarrollo y Arquitectura Incremental

1. **Módulo de Validación de Telemetría (`src/telemetria_drone.py`):** El proyecto establece como núcleo operacional inicial la validación atómica de las tramas de telemetría de un dron individual (`TelemetriaDrone`) y la gestión de sus excepciones de dominio.
2. **Entregable 1 - Fase de Análisis del Problema:** Conforme a la metodología del curso, este primer entregable consolida la etapa formal de **Análisis**:
   - Requisitos Funcionales estructurados en formato estándar (Nombre, Resumen, Entradas, Resultado).
   - Reglas de Negocio claras e inequívocas de la operación aérea.
   - Comprensión del Mundo del Problema (identificación de entidades, atributos y relaciones).
   - Asignación formal de responsabilidades de cada clase.
3. **Perspectiva de Evolución Incremental:** El diseño actual consolida las reglas del componente de telemetría, sentando las bases para incorporar en las siguientes entregas nuevas entidades y módulos del sistema (tales como gestión de flotas, planificación de rutas y control de envíos).


