# 📄 Documento 01: Planteamiento y Descripción General del Problema

**Proyecto:** SkyRoute Drones - Sistema Integrado de Telemetría, Logística y Tráfico Aéreo UAS  
**Asignatura:** Algoritmos de Programación Orientada a Objetos (UDEM)  

---

## 1. Contexto del Problema y Justificación del Negocio
En los últimos años, la logística de entregas de última milla ha experimentado una transformación hacia el uso de **Vehículos Aéreos No Tripulados (VANT / Drones)**. Empresas globales y locales buscan reducir los tiempos de entrega en zonas urbanas congestionadas o áreas de difícil acceso geográfico, especialmente para el transporte urgente de suministros médicos, medicamentos y paquetes livianos.

Sin embargo, el despliegue aéreo comercial de drones presenta desafíos críticos en tres frentes:
1. **Seguridad Operacional y Telemetría:** Cada dron emite tramas periódicas de datos (altitud, coordenadas GPS, estado de motores, nivel de batería). Si una trama errónea o alterada se procesa sin validación previa, se corren riesgos de colisión aérea o accidentes en superficie.
2. **Cumplimiento de la Normativa Aeronáutica:** Las autoridades aéreas imponen restricciones estrictas (ej. altitud máxima de vuelo de 120 metros AGL - *Above Ground Level*, zonas de no vuelo o *Geofencing*, y umbrales mínimos de batería para evitar descensos no planificados).
3. **Gestión de Prioridad Logística:** No todos los paquetes tienen el mismo grado de urgencia. Un suministro médico crítico requiere ventanas de entrega preferenciales sobre un paquete de mensajería convencional.

---

## 2. Definición de la Solución Propuesta
El proyecto **SkyRoute Drones** consiste en el diseño e implementación de un sistema de software basado en la **Programación Orientada a Objetos (POO)** que actúe como una **Central de Operaciones de Tráfico Aéreo y Logística de Drones**.

El sistema procesará las tramas de telemetría emitidas por la flota en tiempo real, validará de forma estricta las condiciones del dron, asignará paquetes según niveles de prioridad y coordinará planes de vuelo seguros.

---

## 3. Alcance del Proyecto
La aplicación incluirá:
* **Módulo de Validación Aeronáutica:** Procesamiento de tramas de telemetría con excepciones de dominio personalizadas.
* **Módulo de Planificación de Rutas:** Cálculo de distancias geográficas reales mediante la **Fórmula de Haversine** y verificación de coordenadas de origen y destino.
* **Módulo de Despacho Logístico:** Gestión de paquetes, asignación de drones disponibles por capacidad de carga y autonomía restante.
* **Módulo de Contingencias y Monitoreo:** Detección de fallas críticas (batería baja, desviación de altitud, pérdida de motor) y ejecución de protocolos de Retorno Automático a Base (**RTH - Return To Home**).

---

## 4. Actores del Sistema
1. **Operador de Torre de Control Aéreo:** Supervisa el estado global de la flota, monitorea alertas de telemetría y autoriza planes de vuelo.
2. **Coordinador Logístico:** Registra paquetes en el sistema, asigna prioridades de envío y consulta el estado de las entregas.
3. **Sistema de Telemetría (Dispositivo IoT):** Emisor automatizado que envía lecturas periódicas del dron a la central de control.
