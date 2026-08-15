# 📦 Guía de Arquitectura, Modularización y Uso (`src/`)

Este documento explica de forma detallada cómo está organizado el código fuente del proyecto **SkyRoute**, cómo funciona el sistema de paquetes y exportaciones en Python, qué hace cada módulo y cómo utilizar las clases en la práctica.

Esta guía está diseñada para que todos los integrantes del equipo (**Alejandro, Valery y Juan Manuel**) comprendan a fondo la estructura y puedan sustentar las decisiones técnicas ante el docente.

---

## 1. ¿Qué es la carpeta `src/` y por qué se usa?

La palabra `src` es la abreviatura universal de **"Source" (Código Fuente)**. En el desarrollo profesional de software con Python, es una buena práctica separar el código del sistema de las carpetas de documentación (`docs/`) y pruebas (`tests/`).

### Beneficios principales:
1. **Orden y Claridad:** Evita tener todos los archivos mezclados en la raíz del proyecto.
2. **Modularidad:** Permite tratar a `src` como un **paquete de Python importable**.
3. **Escalabilidad:** Si en entregas futuras agregamos módulos de *Rutas*, *Flotas* o *Sensores*, cada uno tendrá su propio archivo sin crear un archivo gigante difícil de entender.

---

## 2. Mapa y Estructura Interna de `src/`

```
src/
├── __init__.py           # Archivo maestro del paquete (Exportación limpia)
├── exceptions.py         # Jerarquía de Excepciones de Dominio personalizadas
├── telemetria.py         # Clase principal TelemetriaDrone (Propiedades y Setters)
├── telemetria_drone.py   # Archivo standalone original (con ejecución de demostración)
└── utils/                # Paquete de utilidades y cálculos matemáticos
    ├── __init__.py       # Exportaciones del subpaquete de utilidades
    └── geodesia.py       # Clase CalculadorGeodesico (Fórmula de Haversine)
```

---

## 3. ¿Cómo funciona la exportación con `__init__.py`?

En Python, la presencia de un archivo llamado `__init__.py` dentro de una carpeta le indica al lenguaje que **esa carpeta debe ser tratada como un paquete de módulos importables**.

### ¿Qué problema resuelve nuestro `src/__init__.py`?

#### ❌ Sin exportación centralizada:
Para usar el sistema en un script externo o en las pruebas, tendrías que escribir importaciones largas y recordar en qué archivo exacto vive cada cosa:
```python
from src.telemetria import TelemetriaDrone
from src.exceptions import BateriaInvalidaError, EstadoMotorInvalidoError
from src.utils.geodesia import CalculadorGeodesico
```

#### ✔ Con nuestro `src/__init__.py`:
El archivo `src/__init__.py` importa internamente las clases y define la lista especial `__all__`:
```python
# src/__init__.py
from .exceptions import (
    TelemetriaError,
    BateriaInvalidaError,
    AltitudInvalidaError,
    EstadoMotorInvalidoError,
    CoordenadaInvalidaError,
)
from .utils.geodesia import CalculadorGeodesico
from .telemetria import TelemetriaDrone

__all__ = [
    "TelemetriaDrone",
    "CalculadorGeodesico",
    "TelemetriaError",
    "BateriaInvalidaError",
    "AltitudInvalidaError",
    "EstadoMotorInvalidoError",
    "CoordenadaInvalidaError",
]
```

**Resultado:** Ahora cualquier persona (o las pruebas unitarias) puede importar todo de forma directa, limpia y elegante:
```python
from src import TelemetriaDrone, CalculadorGeodesico, BateriaInvalidaError
```

---

## 4. Análisis Módulo por Módulo: ¿Qué hace, Por qué existe y Para qué sirve?

### A. `src/exceptions.py` (Excepciones de Dominio)
* **¿Qué es?** Un archivo que contiene las clases de error personalizadas de nuestro sistema. Todas heredan de `TelemetriaError`, la cual a su vez hereda de `ValueError`.
* **¿Por qué existe?** Si una batería es `-5%`, lanzar un `ValueError` genérico no le dice al programador qué parte del dron falló. Al crear `BateriaInvalidaError`, el error es explícito y autoexplicativo.
* **Jerarquía implementada:**
  ```
  ValueError (Python)
     └── TelemetriaError (Base del proyecto)
            ├── BateriaInvalidaError
            ├── AltitudInvalidaError
            ├── EstadoMotorInvalidoError
            └── CoordenadaInvalidaError
  ```

---

### B. `src/utils/geodesia.py` (`CalculadorGeodesico`)
* **¿Qué es?** Una clase con métodos estáticos/de clase (`@classmethod`) especializada en cálculos geográficos y trigonometría esférica.
* **¿Por qué se separó de `TelemetriaDrone`? (Principio de Responsabilidad Única - SRP):**
  La clase `TelemetriaDrone` tiene como responsabilidad representar y validar el estado del dron. No debería estar sobrecargada con fórmulas matemáticas complejas de senos, cosenos y radianes. Al poner la fórmula de **Haversine** en `CalculadorGeodesico`:
  1. El código de telemetría queda limpio y fácil de leer.
  2. La fórmula de Haversine puede ser reutilizada en el futuro por cualquier otra clase (por ejemplo, para calcular la longitud total de una ruta).
* **Métodos clave:**
  * `validar_coordenada(coordenada)`: Verifica que la tupla sea `(lat, lon)` con números reales y dentro de $[-90, 90]$ y $[-180, 180]$.
  * `calcular_haversine(origen, destino)`: Aplica la fórmula trigonométrica usando el radio terrestre ($6371.0\,\text{km}$).

---

### C. `src/telemetria.py` (`TelemetriaDrone`)
* **¿Qué es?** La entidad central del proyecto. Representa la lectura instantánea de un dron.
* **¿Cómo aplica el Encapsulamiento en POO?**
  Todos los atributos internos son privados (inician con guión bajo: `_id_dron`, `_bateria`, `_altitud`, `_estado_motores`, `_coordenadas`). El acceso se realiza exclusivamente mediante decoradores `@property` (getters) y sus respectivos setters.
* **Reglas y Validaciones que Aplica:**
  1. **Tipos estrictos:** Se rechaza explícitamente el tipo `bool` (porque en Python `bool` es subclase de `int`).
  2. **Rangos numéricos:** Batería en $[0.0, 100.0]\%$, Altitud en $[0.0, 120.0]\,\text{m}$.
  3. **Coherencia de Motores vs Altitud:**
     - Si $\text{altitud} > 0.0\,\text{m} \implies \text{motores} == \text{'EN\_VUELO'}$.
     - Si $\text{altitud} == 0.0\,\text{m} \implies \text{motores} \in \{\text{'APAGADOS'}, \text{'STANDBY'}, \text{'EMERGENCIA'}\}$.
  4. **Delegación Geodésica:** Al llamar a `dron.calcular_distancia_a_punto(destino)`, el dron le delega el cálculo matemático a `CalculadorGeodesico.calcular_haversine()`.

---

## 5. Ejemplos Prácticos de Uso

### Ejemplo 1: Creación y Lectura de Atributos
```python
from src import TelemetriaDrone

# 1. Instanciación válida de un dron volando sobre Medellín
dron = TelemetriaDrone(
    id_dron="DRN-MDE-01",
    bateria=95.0,
    altitud=30.0,
    estado_motores="EN_VUELO",
    coordenadas=(6.2518, -75.5636)
)

# 2. Acceso a través de getters (@property)
print(f"ID: {dron.id_dron}")          # Salida: DRN-MDE-01
print(f"Batería: {dron.bateria}%")     # Salida: 95.0%
print(f"Altitud: {dron.altitud}m")     # Salida: 30.0m

# 3. Salida formateada con __str__
print(dron)
# Salida: Dron[DRN-MDE-01] - Bat: 95.0% | Alt: 30.0m | Motores: EN_VUELO | GPS: (6.2518, -75.5636)
```

---

### Ejemplo 2: Cálculo de Distancia Geodésica (Haversine)
```python
from src import TelemetriaDrone

dron = TelemetriaDrone("DRN-MDE-01", 90.0, 25.0, "EN_VUELO", (6.2518, -75.5636))

# Coordenadas de destino (Aeropuerto José María Córdova - Rionegro)
aeropuerto_jmc = (6.1644, -75.4276)

distancia = dron.calcular_distancia_a_punto(aeropuerto_jmc)
print(f"Distancia al aeropuerto: {distancia:.2f} km")
# Salida: Distancia al aeropuerto: 17.85 km
```

---

### Ejemplo 3: Captura de Excepciones de Dominio (`try / except`)
```python
from src import TelemetriaDrone, BateriaInvalidaError, EstadoMotorInvalidoError

# Caso A: Intentar crear un dron con batería errónea
try:
    dron_malo = TelemetriaDrone("DRN-02", 150.0, 0.0, "STANDBY", (6.25, -75.56))
except BateriaInvalidaError as e:
    print(f"Fallo de batería detectado: {e}")
    # Salida: Fallo de batería detectado: Batería fuera de rango [0.0%, 100.0%]. Recibido: 150.0%

# Caso B: Intentar elevar un dron en tierra sin encender motores
try:
    dron_tierra = TelemetriaDrone("DRN-03", 100.0, 0.0, "STANDBY", (6.25, -75.56))
    dron_tierra.altitud = 40.0  # Los motores siguen en STANDBY
except EstadoMotorInvalidoError as e:
    print(f"Incoherencia detectada: {e}")
    # Salida: Incoherencia operacional: Con altitud 40.0m > 0, los motores DEBEN estar en 'EN_VUELO'. Recibido: 'STANDBY'.
```

---

### Ejemplo 4: Uso Directo del Módulo Geodésico
```python
from src import CalculadorGeodesico

punto_a = (6.2518, -75.5636)  # Medellín
punto_b = (4.7110, -74.0721)  # Bogotá

distancia_km = CalculadorGeodesico.calcular_haversine(punto_a, punto_b)
print(f"Distancia Medellín - Bogotá: {distancia_km:.2f} km")
# Salida: Distancia Medellín - Bogotá: 237.92 km
```

---

## 6. Preguntas Frecuentes para la Sustentación con el Profesor

Si el docente pregunta sobre la arquitectura del código fuente:

**P: ¿Por qué no dejaron todo el código en un solo archivo `.py`?**  
> *R:* "Para aplicar el principio de modularidad y de Responsabilidad Única (SRP). Separar las excepciones en `exceptions.py`, las fórmulas matemáticas en `utils/geodesia.py` y la entidad en `telemetria.py` hace que el código sea más fácil de mantener, reutilizable y limpio. Además, facilita que el equipo trabaje en Git sin generar conflictos."

**P: ¿Qué ventaja tiene usar `@property` en lugar de crear métodos clásicos como `get_bateria()` y `set_bateria()`?**  
> *R:* "El decorador `@property` es la forma estándar e idiomática (*pythónica*) de encapsulamiento. Permite acceder a los atributos con una sintaxis limpia y natural (`dron.bateria = 80.0`) mientras que por detrás se ejecuta automáticamente toda la lógica de validación del setter."

**P: ¿Cómo se comunican `TelemetriaDrone` y `CalculadorGeodesico`?**  
> *R:* "Mediante una relación de **dependencia / delegación**. Cuando se invoca `dron.calcular_distancia_a_punto(destino)`, la clase `TelemetriaDrone` no implementa la trigonometría directamente, sino que le pasa sus coordenadas a `CalculadorGeodesico.calcular_haversine()`, recibiendo el resultado en kilómetros."

**P: ¿Para qué sirve la lista `__all__` en el `__init__.py`?**  
> *R:* "Define la interfaz pública del paquete. Especifica con precisión qué clases y excepciones se exportan cuando alguien realiza un `from src import *` o cuando importa directamente desde `src`, ocultando detalles internos que no deben ser manipulados."
