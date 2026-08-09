# 📄 Documento 01: Descripción del Problema

**Proyecto:** Sistema de Validación de Telemetría y Gestión de Drones (POO)  
**Institución:** Universidad de Medellín  

---

## Contexto del Problema
Una empresa de entregas de última milla mediante **drones** requiere un sistema de software capaz de procesar y validar las tramas de telemetría emitidas por sus dispositivos en tiempo real. 

Este sistema actúa como la primera línea de defensa para identificar y rechazar lecturas erróneas o incoherentes antes de transmitirlas al servidor central de control de tráfico aéreo.

---

## Características de la Solución
1. **Validación Aeronáutica de Telemetría:** Verificación de parámetros críticos de vuelo como altitud, batería, coordenadas GPS y coherencia del estado de los motores.
2. **Filtrado de Errores y Excepciones:** Clasificación de entradas fuera de norma mediante excepciones de dominio personalizadas.
3. **Cálculo de Rutas y Distancias:** Integración de la fórmula de Haversine para calcular la distancia ortodrómica real hasta el destino del paquete.
