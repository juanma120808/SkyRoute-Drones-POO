# 🧪 Guía de Pruebas Unitarias (`tests/`)

Este directorio contiene la suite de **pruebas unitarias automatizadas** del proyecto **SkyRoute**.

Esta guía explica qué son las pruebas unitarias, cómo funciona el módulo `unittest` de Python, cómo están estructuradas nuestras pruebas y cómo responder a posibles preguntas del docente durante la sustentación.

---

## 1. ¿Qué es una Prueba Unitaria (Unit Test)?

Una **prueba unitaria** es un bloque de código automatizado que prueba la unidad más pequeña y aislada de un programa (por ejemplo, un método, un setter o una función matemática) para comprobar que produce exactamente el resultado esperado bajo diferentes condiciones.

### ¿Por qué las usamos en este proyecto?
1. **Comprobar las Reglas de Negocio:** Nos asegura que si alguien ingresa una batería de `120%`, una altitud negativa de `-10m` o un ID vacío, el sistema rechace el dato disparando la excepción correspondiente.
2. **Garantizar la No Regresión:** Cuando agreguemos nuevas clases en entregas futuras (como rutas o flotas), correr estas pruebas nos confirmará en un segundo que nada de lo que ya funcionaba se rompió.
3. **Validar Casos Límite:** Probar los valores en el borde exacto de los rangos permitidos (ejemplo: batería en `0.0%` y en `100.0%`, altitud en `0.0m` y en `120.0m`).

---

## 2. ¿Cómo funciona el módulo `unittest` de Python?

`unittest` es el framework oficial de pruebas unitarias incluido por defecto en Python (no requiere instalar ninguna librería externa).

### Conceptos clave que debemos dominar:

#### A. La clase `unittest.TestCase`
Cada archivo de prueba define una clase que hereda de `unittest.TestCase`. Esto le da a nuestra clase acceso a métodos de validación llamados **aserciones**.

```python
import unittest

class TestMiModulo(unittest.TestCase):
    # Aquí van los métodos de prueba
```

#### B. El método `setUp(self)`
Es un método especial que **se ejecuta automáticamente antes de cada prueba**. Se utiliza para crear objetos base y preparar el entorno de prueba, evitando repetir código en cada test.

```python
def setUp(self):
    # Se crea un dron nuevo antes de ejecutar cada prueba individual
    self.dron = TelemetriaDrone("DRN-01", 100.0, 50.0, "EN_VUELO", (6.25, -75.56))
```

#### C. Los métodos de prueba (`test_*`)
Todo método que queramos que Python ejecute como prueba **debe iniciar obligatoriamente con la palabra `test_`** (por ejemplo: `test_bateria_valida`, `test_altitud_negativa`). Si no empieza por `test_`, Python lo ignorará.

#### D. Las Aserciones (`assert`) más comunes
Las aserciones son comparaciones que verifican si el resultado del código coincide con lo esperado:

| Aserción | ¿Qué verifica? | Ejemplo en nuestro código |
| :--- | :--- | :--- |
| `self.assertEqual(a, b)` | Comprueba que `a == b`. | `self.assertEqual(self.dron.bateria, 100.0)` |
| `self.assertAlmostEqual(a, b, delta)` | Comprueba que dos números flotantes sean casi iguales (útil para decimales). | `self.assertAlmostEqual(distancia, 237.9, delta=5.0)` |
| `self.assertRaises(Excepcion)` | Comprueba que un bloque de código **lance la excepción esperada** ante datos inválidos. | `with self.assertRaises(BateriaInvalidaError): ...` |
| `self.assertIn(a, b)` | Comprueba que el elemento `a` esté contenido dentro de `b`. | `self.assertIn("DRN-01", str(self.dron))` |

---

## 3. Estructura de Nuestras Pruebas

El directorio `tests/` está organizado en dos archivos principales:

```
tests/
├── __init__.py           # Marca la carpeta como paquete de pruebas
├── test_geodesia.py      # Pruebas para la fórmula de Haversine y validación de coordenadas
└── test_telemetria.py    # Pruebas para los setters, límites de batería, altitud y motores
```

### A. `test_geodesia.py` (Cálculos Geográficos)
* **`test_coordenada_valida`:** Verifica que una tupla válida `(latitud, longitud)` se acepte correctamente.
* **`test_coordenada_tipo_invalido`:** Verifica que listas o tuplas con más o menos de 2 elementos sean rechazadas.
* **`test_coordenada_fuera_de_rango`:** Verifica que latitudes $> 90^\circ$ o $<-90^\circ$ y longitudes fuera de $[-180^\circ, 180^\circ]$ lancen `CoordenadaInvalidaError`.
* **`test_calculo_haversine_medellin_bogota`:** Calcula la distancia entre Medellín y Bogotá y comprueba que el resultado sea aproximadamente $237.9\,\text{km}$.
* **`test_calculo_haversine_mismo_punto`:** Verifica que la distancia entre un punto y sí mismo sea exactamente $0.0\,\text{km}$.

### B. `test_telemetria.py` (Validaciones de la Entidad Drone)
* **Identificador:** Comprueba que no se permitan cadenas vacías (`""` o `"   "`).
* **Batería:** Comprueba que se acepten valores en $[0.0, 100.0]\%$ y se rechacen valores como `-0.1` o `100.1`.
* **Altitud:** Comprueba que se acepten valores en $[0.0, 120.0]\,\text{m}$ y se rechacen valores $> 120.0\,\text{m}$ o $< 0.0\,\text{m}$.
* **Coherencia de Motores vs Altitud:** Comprueba que si la altitud es $> 0$, los motores no puedan ser `STANDBY` ni `APAGADOS`, y que en tierra (`0.0m`) no puedan estar en `EN_VUELO`.
* **Blindaje de Mutaciones:** Comprueba que si el dron ya está creado en tierra y luego se modifica `dron.altitud = 50.0`, el setter rechace el cambio si los motores no se han encendido a `EN_VUELO`.
* **Métodos Mágicos:** Comprueba que `__str__` y `__repr__` devuelvan el formato legible esperado.

---

## 4. ¿Cómo ejecutar las pruebas desde la terminal?

### Para ejecutar TODAS las pruebas del proyecto:
Abre la terminal en la raíz del repositorio (`SkyRoute-Drones-POO/`) y escribe:

```bash
python -m unittest discover tests
```

#### Explicación del comando:
* `python -m unittest`: Le dice a Python que ejecute su módulo interno de pruebas.
* `discover tests`: Le indica que busque automáticamente dentro de la carpeta `tests/` todos los archivos que comiencen por `test_*.py` y ejecute todas sus funciones.

### Salida esperada en consola:
```
....................
----------------------------------------------------------------------
Ran 20 tests in 0.001s

OK
```
* Cada punto (`.`) representa una prueba que pasó exitosamente (20 puntos = 20 pruebas aprobadas).
* `OK` al final confirma que no hubo ningún error ni fallo.

### Para ejecutar un solo archivo de prueba:
```bash
python -m unittest tests/test_telemetria.py
```
o
```bash
python -m unittest tests/test_geodesia.py
```

---

## 5. Preguntas Frecuentes para la Sustentación con el Profesor

Si el docente pregunta sobre las pruebas durante la revisión, aquí están las respuestas claras:

**P: ¿Por qué crearon pruebas unitarias si el ejercicio solo pedía la clase?**  
> *R:* "Para aplicar buenas prácticas de ingeniería de software. Las pruebas nos permiten validar automáticamente que todas las reglas de negocio (rangos de batería, límites de altitud y la coherencia con los motores) se cumplan y que ningún dato inválido pueda romper el sistema."

**P: ¿Qué hace `with self.assertRaises(BateriaInvalidaError):`?**  
> *R:* "Indica que el código dentro de ese bloque `with` está obligado a fallar lanzando esa excepción específica. Si el código lanza la excepción correcta, la prueba pasa; si no la lanza o lanza otro tipo de error, la prueba falla porque significa que la validación no está funcionando."

**P: ¿Por qué usamos `assertAlmostEqual` en el cálculo de Haversine en vez de `assertEqual`?**  
> *R:* "Porque los cálculos trigonométricos con funciones como seno, coseno y radianes generan números con muchos decimales en coma flotante (`float`). `assertAlmostEqual` nos permite comparar con un margen de tolerancia (`delta`), evitando que diferencias mínimas en los últimos decimales hagan fallar la prueba."
