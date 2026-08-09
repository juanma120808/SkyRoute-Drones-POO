# Documento 02: Especificación de Requisitos y Reglas de Negocio

**Proyecto:** Sistema de Gestión y Telemetría para Drones  
**Asignatura:** Algoritmos de Programación Orientada a Objetos  
**Institución:** Universidad de Medellín  

---

## 1. Reglas de Negocio del Sistema

Basado en el planteamiento inicial de `ejercicio_1_poo.py`, se establecen las siguientes reglas esenciales:

1. **Identificación:** Todo dispositivo posee un identificador único alfanumérico. No se admiten cadenas vacías.
2. **Nivel de Batería:** Expresado en porcentaje dentro del rango `[0.0, 100.0]`. Valores fuera de este rango disparan una excepción de dominio.
3. **Límite de Altitud:** Expresado en metros. Por regulación, la altitud debe situarse entre `0.0` metros (superficie) y `120.0` metros (límite regulatorio).
4. **Coherencia de Estado:**
   - Altitudes superiores a `0.0` metros requieren obligatoriamente que los motores estén en estado `'EN_VUELO'`.
   - Altitud igual a `0.0` metros no admite el estado `'EN_VUELO'` (debe estar en `'APAGADOS'`, `'STANDBY'` o `'EMERGENCIA'`).
   - Los estados permitidos para los motores son estrictamente: `'APAGADOS'`, `'STANDBY'`, `'EN_VUELO'`, `'EMERGENCIA'`.
5. **Coordenadas Geográficas:** Formateadas como par `(latitud, longitud)` dentro de rangos válidos de latitud `[-90.0, 90.0]` y longitud `[-180.0, 180.0]`.

---

## 2. Requisitos Funcionales

* **RF-01 (Procesamiento y Validación de Telemetría):** El sistema debe recibir los datos de cada trama y evaluar su validez antes de almacenarlos.
* **RF-02 (Manejo de Excepciones de Dominio):** El sistema debe interrumpir la lectura y notificar errores específicos cuando una regla de negocio sea infringida.
* **RF-03 (Cálculo Ortodrómico):** El sistema debe permitir estimar la distancia en kilómetros hacia un punto geográfico utilizando la fórmula de Haversine.
* **RF-04 (Salida por Consola):** El sistema debe ofrecer representaciones legibles de las tramas para inspección por consola.
