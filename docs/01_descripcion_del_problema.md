# Documento 01: Descripción del Problema

**Proyecto:** Sistema de Gestión y Telemetría para Drones  
**Asignatura:** Algoritmos de Programación Orientada a Objetos  
**Institución:** Universidad de Medellín  

---

## Contexto del Problema

Una empresa dedicada al transporte y logística mediante aeronaves no tripuladas (drones) requiere un módulo de software capaz de recibir, procesar y validar tramas de telemetría en tiempo real.

En operaciones aeronáuticas, la integridad de los datos recibidos de los sensores es fundamental. El software debe actuar como una capa de validación previa que identifique e impida el procesamiento de tramas con datos inconsistentes o fuera de los rangos operacionales permitidos (como niveles inválidos de batería, altitudes fuera de norma o incoherencias entre el estado de los motores y la altitud del dispositivo).

---

## Alcance Inicial

El proyecto toma como referencia el ejercicio práctico `ejercicio_1_poo.py` desarrollado previamente en la asignatura. A partir de esa guía inicial, se plantea estructurar un sistema orientado a objetos que responda a los siguientes frentes:

1. **Validación de Telemetría:** Verificación de parámetros de vuelo y disparo de excepciones de dominio ante lecturas erróneas.
2. **Cálculo de Distancias:** Estimación de distancias ortodrómicas a puntos de destino utilizando la fórmula de Haversine.
3. **Representación y Formato:** Estructuración de datos legible para operadores de consola y depuración interna.
