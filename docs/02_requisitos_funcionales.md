# 📋 Documento 02: Especificación de Requisitos Funcionales y Reglas de Negocio

**Proyecto:** Sistema de Validación de Telemetría y Gestión de Drones (POO)  
**Institución:** Universidad de Medellín  

---

## 1. Reglas de Negocio del Sistema
1. **Identificación del Dron:** Cada dron posee un identificador único alfanumérico. No se permiten cadenas vacías.
2. **Nivel de Batería:** Debe fluctuar estrictamente entre `0.0` y `100.0` (porcentaje). Cualquier valor fuera de este rango dispara la excepción `BateriaInvalidaError`.
3. **Límite de Altitud:** Medido en metros. Por regulación aeronáutica no puede ser menor a `0.0` metros (tierra) ni superior a `120.0` metros. De lo contrario, dispara `AltitudInvalidaError`.
4. **Coherencia de Estado:**
   - Si la altitud es `> 0.0` metros, el estado de los motores debe ser obligatoriamente `'EN_VUELO'`.
   - Si la altitud es `0.0` metros, el estado no puede ser `'EN_VUELO'` (debe ser `'APAGADOS'`, `'STANDBY'` o `'EMERGENCIA'`).
   - Los únicos estados válidos son: `'APAGADOS'`, `'STANDBY'`, `'EN_VUELO'`, `'EMERGENCIA'`.
5. **Coordenadas Geográficas:** Debe ser una tupla `(latitud, longitud)` donde la latitud está en `[-90.0, 90.0]` y la longitud en `[-180.0, 180.0]`.
6. **Navegación y Distancia:** Cálculo de la distancia ortodrómica a un punto de destino mediante la **Fórmula de Haversine**.

---

## 2. Requisitos Funcionales
* **RF-01 (Validación de trama de telemetría):** Procesar y validar los atributos privados de la trama con decoradores `@property` y setters de validación.
* **RF-02 (Gestión de excepciones de dominio):** Disparar excepciones personalizadas derivadas de `ValueError` cuando se violen las reglas de negocio.
* **RF-03 (Cálculo de distancia a destino):** Calcular la distancia en km hasta un punto GPS utilizando la fórmula de Haversine.
* **RF-04 (Representación de consola):** Implementar los métodos mágicos `__str__` para operadores y `__repr__` para depuración.
