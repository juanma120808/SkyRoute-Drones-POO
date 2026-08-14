# Documento 02: Requisitos Funcionales y Reglas de Negocio

**Proyecto:** SkyRoute - Sistema de Gestión y Telemetría para Drones  
**Asignatura:** Algoritmos de Programación Orientada a Objetos  
**Institución:** Universidad de Medellín (UDEM)  

---

## 1. Reglas de Negocio (Restricciones de Dominio)

1. **Identificador Único (`id_dron`):** Cadena alfanumérica no vacía.
2. **Nivel de Batería (`bateria`):** Flotante en rango $[0.0, 100.0]\%$.
3. **Límite de Altitud (`altitud`):** Flotante en metros $[0.0, 120.0]\,m$.
4. **Coherencia Estado de Motores vs Altitud:**
   - Si $\text{altitud} > 0.0$, $\text{estado\_motores} == \text{'EN\_VUELO'}$.
   - Si $\text{altitud} == 0.0$, $\text{estado\_motores} \neq \text{'EN\_VUELO'}$ (`'APAGADOS'`, `'STANDBY'`, `'EMERGENCIA'`).
5. **Coordenadas Geográficas (`coordenadas`):** Par $(\text{latitud}, \text{longitud})$ con $\text{latitud} \in [-90.0, 90.0]$ y $\text{longitud} \in [-180.0, 180.0]$.

---

## 2. Requisitos Funcionales (Formato Oficial UDEM)

### **R1: Validar e Instanciar Trama de Telemetría**
* **Nombre:** Validar e Instanciar Trama de Telemetría
* **Resumen:** Actor: Operador / Sensor. El sistema recibe la información reportada por un dron y valida que cumpla con los tipos de datos y todas las reglas de negocio antes de registrar la trama.
* **Entradas:** `id_dron` (str), `bateria` (float), `altitud` (float), `estado_motores` (str), `coordenadas` (tuple[float, float]).
* **Resultado:** Objeto `TelemetriaDrone` correctamente instanciado y validado. Si algún dato es inválido, no se crea la trama y se genera la excepción de dominio correspondiente.

---

### **R2: Notificar Excepciones de Dominio**
* **Nombre:** Notificar Excepciones de Dominio
* **Resumen:** Actor: Sistema / Operador. Al detectar una violación a las reglas de negocio, el sistema interrumpe el procesamiento y genera una excepción personalizada con detalles específicos del fallo.
* **Entradas:** Datos fuera de norma ingresados durante la instanciación o modificación.
* **Resultado:** Disparo de `BateriaInvalidaError`, `AltitudInvalidaError`, `EstadoMotorInvalidoError` o `CoordenadaInvalidaError`.

---

### **R3: Calcular Distancia Ortodrómica a Destino**
* **Nombre:** Calcular Distancia Ortodrómica a Destino
* **Resumen:** Actor: Operador de Vuelo. Calcula la distancia en kilómetros entre la ubicación actual del dron y una coordenada dada utilizando la fórmula de Haversine.
* **Entradas:** Coordenada de destino `(latitud, longitud)` (tuple[float, float]).
* **Resultado:** Valor numérico (`float`) con la distancia calculada en kilómetros.

---

### **R4: Consultar Formato de Consola e Inspección Técnica**
* **Nombre:** Consultar Formato de Consola e Inspección Técnica
* **Resumen:** Actor: Operador / Desarrollador. Obtiene una representación textual estructurada de la telemetría del dron para monitoreo rápido en consola (`__str__`) o depuración (`__repr__`).
* **Entradas:** Ninguna (opera sobre la instancia del dron).
* **Resultado:** Cadena de texto formateada con los datos de telemetría.

