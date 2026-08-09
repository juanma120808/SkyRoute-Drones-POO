# 📋 Documento 02: Especificación de Requisitos Funcionales y Prototipos CLI

**Proyecto:** SkyRoute Drones - Sistema Integrado de Telemetría, Logística y Tráfico Aéreo UAS  
**Asignatura:** Algoritmos de Programación Orientada a Objetos (UDEM)  

---

## 1. Requisitos Funcionales Generales

| Código | Nombre del Requisito | Descripción | Prioridad |
| :--- | :--- | :--- | :--- |
| **RF-01** | Registro de Flota de Drones | El sistema debe permitir registrar drones especificando su ID único, modelo, capacidad máxima de carga (kg) y batería inicial. | Alta |
| **RF-02** | Registro de Paquetes | El sistema debe permitir ingresar paquetes indicando peso, dirección de destino (coordenadas GPS) y tipo de paquete. | Alta |
| **RF-03** | Consulta de Estado de Flota | El sistema debe mostrar en consola una lista detallada con la ubicación, batería, altitud y estado de cada dron en la flota. | Media |
| **RF-04** | Eliminación / Retiro de Dron | El sistema debe permitir deshabilitar o remover un dron del servicio en caso de mantenimiento. | Baja |

---

## 2. Requisitos Funcionales Innovadores (Por Integrante del Equipo)

### 🌟 RF-INV-01: Validación de Telemetría, Geofencing y Cálculo Ortodrómico (Haversine)
* **Responsable:** **Juan Manuel Pava Higuita**
* **Descripción:** 
  El sistema debe procesar y validar en tiempo real las tramas de telemetría emitidas por los drones. 
  - Debe verificar que la batería esté en el rango $[0.0, 100.0]\%$.
  - Debe validar la altitud dentro del límite regulatorio $[0.0, 120.0]$ metros.
  - Debe aplicar la **Fórmula de Haversine** para calcular la distancia ortodrómica real en kilómetros desde la posición actual del dron hasta el destino del paquete.
  - Debe validar zonas de no vuelo (**Geofencing**) comprobando si las coordenadas del dron violan polígonos restringidos.
* **Manejo de Excepciones:** Disparar excepciones de dominio (`BateriaInvalidaError`, `AltitudInvalidaError`, `GeofenceViolationError`).

---

### 🌟 RF-INV-02: Gestión Logística de Envíos Críticos y Autonomía Energética Dinámica
* **Responsable:** **Valery Arboleda Ardila**
* **Descripción:**
  El sistema debe clasificar los paquetes según su nivel de prioridad (`NORMAL`, `URGENTE`, `CRITICO_MEDICO`).
  - Para entregas clasificadas como `CRITICO_MEDICO`, el sistema debe reorganizar automáticamente la cola de despachos e interrumpe la asignación regular para enviar el dron más cercano con suficiente autonomía.
  - Debe calcular la **Autonomía Energética Dinámica**: estima la tasa de consumo de batería ($\%/km$) en función del peso del paquete cargado y la velocidad teórica del viento, impidiendo el despegue si el consumo estimado supera la batería disponible con un margen de seguridad del $20\%$.

---

### 🌟 RF-INV-03: Protocolo de Contingencias Aéreas y Retorno Automático a Base (RTH)
* **Responsable:** **Alejandro García Jiménez**
* **Descripción:**
  El sistema debe evaluar constantemente la coherencia del estado del dron.
  - **Regla de Coherencia:** Si la altitud es $> 0.0$ metros, los motores deben estar obligatoriamente en `'EN_VUELO'`. Si la altitud es $0.0$, el estado no puede ser `'EN_VUELO'` (debe ser `'APAGADOS'`, `'STANDBY'` o `'EMERGENCIA'`).
  - En caso de detectar batería $< 15\%$, falla de motor o pérdida de señal de telemetría durante el vuelo, el sistema activa automáticamente el protocolo de emergencia **RTH (Return To Home)**, forzando la reorientación del dron hacia la base más cercana y actualizando su estado a `'EMERGENCIA'`.

---

## 3. Prototipo de Interfaz de Consola (Ejemplo de Ejecución)

```
======================================================================
               🛸 SKYROUTE DRONES - TORRE DE CONTROL V1.0             
======================================================================
1. Registrar Dron en Flota
2. Registrar Paquete de Entrega
3. Procesar Trama de Telemetria (Validacion & Haversine) [Juan Pava]
4. Asignar Despacho Critico / Estimacion Energetica   [Valery Arboleda]
5. Ejecutar Simulación de Vuelo y Protocolo RTH        [Alejandro García]
6. Consultar Estado Global de la Flota
7. Salir
======================================================================
Seleccione una opcion (1-7): 3

--- PROCESANDO TELEMETRIA EN TIEMPO REAL ---
[INFO] Dron ID: DRON-01 | Lat: 6.2314, Lon: -75.5812 | Alt: 45.0m | Bat: 88.5%
[HAVERSINE] Distancia al punto de entrega: 3.42 km
[VALIDACION] Status: OK | Telemetria valida y dentro de zona permitida.
```
