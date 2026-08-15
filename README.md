# 🛸 SkyRoute: Sistema de Gestión y Telemetría para Drones

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 👥 Información Académica y Equipo
* **Institución:** Universidad de Medellín (UDEM)
* **Asignatura:** Algoritmos de Programación Orientada a Objetos
* **Docente:** Mario Alejandro Saldarriaga (Grupo 62)
* **Integrantes:**
  * Alejandro García Jiménez
  * Juan Manuel Pava Higuita
  * Valery Arboleda Ardila

---

## 📌 Planteamiento del Problema
En operaciones de logística y transporte con drones, la precisión y validez de los datos de telemetría emitidos por los sensores es fundamental. 

Este proyecto implementa el módulo central de telemetría (**SkyRoute**), el cual procesa y valida en tiempo real las tramas de vuelo para asegurar que los datos cumplan con las restricciones físicas y la normativa aeronáutica antes de ser procesados por los sistemas de control.

### 🛡️ Reglas de Negocio Implementadas
1. **Identificador del Dron (`id_dron`):** Cadena de texto no vacía.
2. **Nivel de Batería (`bateria`):** Porcentaje delimitado estrictamente en el rango $[0.0, 100.0]\%$.
3. **Límite de Altitud (`altitud`):** Altura en metros sobre el suelo en el rango $[0.0, 120.0]\,m$ (techo aeronáutico legal).
4. **Coherencia de Motores vs Altitud:**
   - Si $\text{altitud} > 0.0\,m \implies \text{estado\_motores}$ debe ser `'EN_VUELO'`.
   - Si $\text{altitud} == 0.0\,m \implies \text{estado\_motores}$ debe ser `'APAGADOS'`, `'STANDBY'` o `'EMERGENCIA'`.
   - Los estados válidos para los motores son estrictamente: `{'APAGADOS', 'STANDBY', 'EN_VUELO', 'EMERGENCIA'}`.
5. **Coordenadas Geográficas (`coordenadas`):** Tupla `(latitud, longitud)` dentro de los rangos válidos $[-90.0, 90.0]$ y $[-180.0, 180.0]$.
6. **Cálculo de Distancia a Destino:** Cálculo de distancia ortodrómica en kilómetros utilizando la **Fórmula de Haversine** ($R = 6371.0\,km$).

---

## 📂 Estructura del Proyecto

```
SkyRoute-Drones-POO/
├── docs/                             # Documentación formal de análisis (Metodología UDEM)
│   ├── 01_descripcion_del_problema.md# Contexto del problema
│   ├── 02_requisitos_funcionales.md  # Requisitos Funcionales y Reglas de Negocio
│   ├── 03_modelo_del_mundo_uml.md    # Entidades y Diagrama de Clases UML
│   └── ANALISIS_DEL_PROBLEMA.md      # Documento consolidado del Entregable 1
│
├── src/                              # Código fuente del sistema
│   ├── __init__.py                   # Exportaciones del paquete
│   ├── exceptions.py                 # Jerarquía de Excepciones de Dominio
│   ├── telemetria.py                 # Clase TelemetriaDrone (Propiedades y Setters)
│   ├── telemetria_drone.py           # Script standalone de referencia y verificación
│   └── utils/                        # Módulo de utilidades matemáticas
│       ├── __init__.py
│       └── geodesia.py               # CalculadorGeodesico (Fórmula de Haversine)
│
├── tests/                            # Suite de Pruebas Unitarias
│   ├── README.md                     # Guía didáctica y explicación de las pruebas
│   ├── __init__.py
│   ├── test_geodesia.py              # Pruebas del módulo de geodesia
│   └── test_telemetria.py            # Pruebas de validación de telemetría
│
├── requirements.txt                  # Dependencias opcionales de desarrollo
├── LICENSE                           # Licencia MIT
└── README.md                         # Este documento
```

---

## 💻 Ejemplos de Uso

### 1. Creación y Consulta de un Dron
```python
from src import TelemetriaDrone

# Crear una lectura de telemetría válida
dron = TelemetriaDrone(
    id_dron="DRN-COL-501",
    bateria=92.4,
    altitud=45.0,
    estado_motores="EN_VUELO",
    coordenadas=(6.2518, -75.5636)
)

print(dron)
# Salida: Dron[DRN-COL-501] - Bat: 92.4% | Alt: 45.0m | Motores: EN_VUELO | GPS: (6.2518, -75.5636)
```

### 2. Cálculo de Distancia a un Destino (Haversine)
```python
# Calcular distancia hacia Bogotá (4.7110, -74.0721)
destino_bogota = (4.7110, -74.0721)
distancia = dron.calcular_distancia_a_punto(destino_bogota)

print(f"Distancia: {distancia:.2f} km")
# Salida: Distancia: 237.92 km
```

### 3. Manejo de Excepciones de Dominio
```python
from src import TelemetriaDrone, EstadoMotorInvalidoError

try:
    # Intentar asignar altitud positiva con motores en STANDBY
    dron_tierra = TelemetriaDrone("DRN-GROUND", 100.0, 0.0, "STANDBY", (6.25, -75.56))
    dron_tierra.altitud = 50.0  # Lanza EstadoMotorInvalidoError
except EstadoMotorInvalidoError as error:
    print(f"Validación activada: {error}")
```
