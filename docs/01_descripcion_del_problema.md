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

## 2. Historial de Desarrollo y Punto de Partida

1. **Ejercicio Base de Referencia (`ejercicio_1_poo.py`):** El proyecto parte formalmente del ejercicio práctico inicial realizado en clase, el cual resolvió la validación atómica de la trama de telemetría de un dron individual (`TelemetriaDrone`) y la gestión de sus excepciones de dominio.
2. **Entregable 1 - Fase de Análisis del Problema:** Conforme a la metodología impartida en la asignatura (basada en el documento *Etapa de Análisis del Problema* y el *Caso de Estudio Tienda de Libros*), este primer entregable consolida estrictamente la fase de **Análisis**:
   - Requisitos Funcionales estructurados en formato de tabla (Nombre, Resumen, Entradas, Resultado).
   - Reglas de Negocio claras e inequívocas.
   - Comprensión del Mundo del Problema (identificación de entidades, atributos y relaciones).
   - Asignación de responsabilidades de cada clase.
3. **Perspectiva de Evolución (Futuras Entregas):** El diseño actual se mantiene fiel a lo verificado (ejercicio base), sentando la base para que en entregas posteriores se extienda el dominio (ej. gestión de flotas, planes de vuelo, carritos de paquetes/entregas) a medida que se definan en clase sus entidades, propiedades y funciones.

