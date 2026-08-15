# Documento 01: Descripción e Historial del Problema

**Proyecto:** SkyRoute - Sistema de Gestión y Telemetría para Drones  
**Asignatura:** Algoritmos de Programación Orientada a Objetos  
**Institución:** Universidad de Medellín (UDEM)  
**Semestre:** 2026-2  
**Docente:** Mario Alejandro Saldarriaga (Grupo 62)  
**Equipo:** Alejandro García Jiménez, Juan Manuel Pava Higuita, Valery Arboleda Ardila  

---

## 1. Contexto del Problema

Una empresa dedicada al transporte y logística mediante drones requiere un módulo de software capaz de recibir, procesar y validar tramas de telemetría emitidas en tiempo real por los sensores a bordo.

En operaciones de vuelo, la validez de los datos recibidos es fundamental. El software se encarga de recibir los datos y verificar que cumplan con los rangos permitidos y las restricciones físicas (por ejemplo, que la batería esté en los rangos adecuados, que la altitud no supere los límites legales y que el estado de los motores sea coherente con la altura del dron).

---

## 2. Historial de Desarrollo y Evolución del Proyecto

1. **Módulo de Telemetría y Validaciones:** Se implementó la clase `TelemetriaDrone` con encapsulamiento estricto (`@property`), validaciones de tipo, control de excepciones de dominio y cálculo de distancias ortodrómicas con la fórmula de Haversine.
2. **Entregable 1 - Análisis del Problema:** Conforme a la metodología del curso de Algoritmos de POO de la UDEM, se formalizan los siguientes puntos:
   - Requisitos Funcionales del sistema (RF-01 a RF-04).
   - Reglas de Negocio claras del dominio aeronáutico.
   - Modelo del Mundo, asignación de responsabilidades de las clases y Diagrama UML.
