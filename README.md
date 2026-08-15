# 🛸 SkyRoute: Sistema de Gestión y Telemetría para Drones

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-20%2F20%20Passing-brightgreen.svg)]()
[![Code Style](https://img.shields.io/badge/POO-Strict%20Encapsulation-blueviolet.svg)]()
[![Academic](https://img.shields.io/badge/UDEM-2026--2-red.svg)]()

> **Módulo de Primera Línea de Defensa en Telemetría Aeronáutica para Logística de Última Milla.**

---

## 👥 Información Académica y Equipo
* **Institución:** Universidad de Medellín (UDEM)
* **Asignatura:** Algoritmos de Programación Orientada a Objetos
* **Docente:** Mario Alejandro Saldarriaga (Grupo 62)
* **Equipo de Trabajo:**
  * **Juan Manuel Pava Higuita**
  * **Alejandro García Jiménez**
  * **Valery Arboleda Ardila**

---

## 📌 Planteamiento del Problema
En operaciones de logística mediante aeronaves no tripuladas (drones), la integridad de las tramas de datos emitidas por los sensores a bordo es fundamental para la seguridad del espacio aéreo. 

**SkyRoute Telemetry Core** opera como un middleware de validación estricta que recibe, procesa y verifica las lecturas de telemetría en tiempo real antes de remitirlas al centro de control de tráfico aéreo, garantizando que ninguna lectura corrupta o incoherente entre en el flujo de toma de decisiones.

### 🛡️ Reglas de Negocio Implementadas:
1. **Identificador Único (`id_dron`):** Cadena de texto no vacía.
2. **Nivel de Batería (`bateria`):** Rango estrictamente delimitado en $[0.0, 100.0]\%$. Exclusión de tipos booleanos.
3. **Límite de Altitud (`altitud`):** Rango de $[0.0, 120.0]\,m$ (techo aeronáutico regulatorio). Exclusión de tipos booleanos.
4. **Coherencia Bidireccional de Motores vs Altitud:**
   - Si $\text{altitud} > 0.0\,m \implies \text{motores} == \text{'EN\_VUELO'}$.
   - Si $\text{altitud} == 0.0\,m \implies \text{motores} \neq \text{'EN\_VUELO'}$ (valores válidos: `'APAGADOS'`, `'STANDBY'`, `'EMERGENCIA'`).
   - Esta coherencia se preserva tanto en la creación como en modificaciones posteriores.
5. **Geolocalización:** Tupla `(latitud, longitud)` dentro de rangos legales $[-90.0, 90.0]$ y $[-180.0, 180.0]$.
6. **Navegación Geodésica:** Cálculo ortodrómico a destino mediante la **Fórmula de Haversine** ($R = 6371.0\,km$).

---

## 📂 Arquitectura del Repositorio

```
SkyRoute-Drones-POO/
├── docs/                             # Documentación formal de análisis (Metodología UDEM)
│   ├── 01_descripcion_del_problema.md# Contexto del problema y evolución
│   ├── 02_requisitos_funcionales.md  # Requisitos Funcionales normalizados y Reglas
│   ├── 03_modelo_del_mundo_uml.md    # Entidades, responsabilidades y diagrama UML
│   └── ANALISIS_DEL_PROBLEMA.md      # Documento maestro consolidado (Entregable 1)
│
├── src/                              # Capa de Código Fuente Modular
│   ├── __init__.py                   # Exportaciones ergonómicas del paquete
│   ├── exceptions.py                 # Jerarquía de Excepciones de Dominio
│   ├── telemetria.py                 # Entidad TelemetriaDrone (Propiedades y Setters)
│   ├── telemetria_drone.py           # Script standalone de referencia y verificación
│   └── utils/                        # Módulo de utilidades matemáticas
│       ├── __init__.py
│       └── geodesia.py               # CalculadorGeodesico (Fórmula de Haversine)
│
├── tests/                            # Suite de Pruebas Unitarias Automatizadas
│   ├── __init__.py
│   ├── test_geodesia.py              # Tests de precisión matemática Haversine
│   └── test_telemetria.py            # Tests de validación de negocio y casos de borde
│
├── requirements.txt                  # Dependencias de testing y linters
├── LICENSE                           # Licencia MIT
└── README.md                         # Este documento
```

---

## 💻 Ejemplos de Uso en Código

### 1. Instanciación y Consulta de Telemetría
```python
from src import TelemetriaDrone

# Crear una trama válida de un dron en vuelo sobre Medellín
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

### 2. Cálculo Geodésico de Distancia (Haversine)
```python
# Calcular distancia hacia el aeropuerto El Dorado de Bogotá
bogota_gps = (4.7110, -74.0721)
distancia_km = dron.calcular_distancia_a_punto(bogota_gps)

print(f"Distancia a Bogotá: {distancia_km:.2f} km")
# Salida: Distancia a Bogotá: 237.92 km
```

### 3. Captura de Excepciones de Dominio
```python
from src import TelemetriaDrone, EstadoMotorInvalidoError

try:
    # Intento de elevar altitud con motores en STANDBY
    dron_tierra = TelemetriaDrone("DRN-GROUND", 100.0, 0.0, "STANDBY", (6.25, -75.56))
    dron_tierra.altitud = 60.0  # Dispara excepción de validación cruzada
except EstadoMotorInvalidoError as e:
    print(f"Error operacional interceptado: {e}")
```

---

## 🧪 Ejecución de Pruebas Automatizadas

El proyecto cuenta con una suite completa de **20 pruebas unitarias** que evalúan casos límite, rechazo de tipos erróneos y coherencia física.

Para ejecutar todas las pruebas:
```bash
python -m unittest discover tests
```

Salida esperada:
```
....................
----------------------------------------------------------------------
Ran 20 tests in 0.001s

OK
```

---

## 🤝 Reparto de Responsabilidades para el Equipo

| Integrante | Módulo Principal en Git | Tareas Clave |
| :--- | :--- | :--- |
| **Juan Manuel Pava** | `src/telemetria.py` | Encapsulamiento, validación cruzada bidireccional y dunder methods. |
| **Alejandro García** | `src/utils/`, `src/exceptions.py` | Algoritmo de Haversine y jerarquía de excepciones de dominio. |
| **Valery Arboleda** | `tests/`, `docs/` | Suite automatizada de pruebas unitarias y documentación formal UDEM. |
