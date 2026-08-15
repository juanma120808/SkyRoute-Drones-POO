# Documento 02: Requisitos Funcionales y Reglas de Negocio

**Proyecto:** SkyRoute - Sistema de Gestión y Telemetría para Drones  
**Asignatura:** Algoritmos de Programación Orientada a Objetos  
**Institución:** Universidad de Medellín (UDEM)  

---

## 1. Reglas de Negocio del Sistema (Restricciones de Dominio)

1. **Identificador Único (`id_dron`):** Cadena alfanumérica no vacía (`str`). No se permiten espacios en blanco puros.
2. **Nivel de Batería (`bateria`):** Número real en porcentaje delimitado estrictamente en $[0.0, 100.0]\%$.
3. **Límite de Altitud (`altitud`):** Medida en metros sobre el nivel del suelo en el rango $[0.0, 120.0]\,m$ (techo aeronáutico regulatorio).
4. **Coherencia de Motores vs Altitud:**
   - Si $\text{altitud} > 0.0\,m \implies \text{estado\_motores}$ debe ser obligatoriamente `'EN_VUELO'`.
   - Si $\text{altitud} == 0.0\,m$ (en tierra) $\implies \text{estado\_motores}$ no puede ser `'EN_VUELO'` (debe ser `'APAGADOS'`, `'STANDBY'` o `'EMERGENCIA'`).
   - El conjunto de estados válidos para los motores es estrictamente: `{'APAGADOS', 'STANDBY', 'EN_VUELO', 'EMERGENCIA'}`.
5. **Coordenadas Geográficas (`coordenadas`):** Tupla de dos números reales $(\text{latitud}, \text{longitud})$ con $\text{latitud} \in [-90.0, 90.0]$ y $\text{longitud} \in [-180.0, 180.0]$.
6. **Cálculo Geodésico:** La distancia a un destino geográfico se calcula mediante la fórmula de Haversine asumiendo un radio terrestre de $6371.0\,km$.

---

## 2. Requisitos Funcionales (Formato Oficial UDEM)

### **RF-01: Validar e Instanciar Trama de Telemetría**
* **Nombre:** Validar e Instanciar Trama de Telemetría
* **Resumen:** **Actor:** Sensor / Operador de Vuelo. El sistema recibe los datos crudos de telemetría de una aeronave y valida tipos de datos, rangos y coherencia física antes de instanciar el objeto `TelemetriaDrone`.
* **Entradas:** `id_dron` (str), `bateria` (float), `altitud` (float), `estado_motores` (str), `coordenadas` (tuple[float, float]).
* **Resultado:** Objeto `TelemetriaDrone` correctamente creado con atributos privados y accesores protegidos.

---

### **RF-02: Notificar Excepciones de Dominio Específicas**
* **Nombre:** Notificar Excepciones de Dominio
* **Resumen:** **Actor:** Sistema / Operador. Al detectar cualquier violación a las reglas de negocio, el sistema interrumpe la operación de forma controlada y dispara la excepción correspondiente con un mensaje descriptivo del fallo.
* **Entradas:** Parámetros inválidos pasados durante la creación o modificación de atributos.
* **Resultado:** Disparo de `BateriaInvalidaError`, `AltitudInvalidaError`, `EstadoMotorInvalidoError` o `CoordenadaInvalidaError`.

---

### **RF-03: Calcular Distancia Ortodrómica a Destino**
* **Nombre:** Calcular Distancia Ortodrómica a Destino
* **Resumen:** **Actor:** Operador de Vuelo. Calcula la distancia geodésica en kilómetros entre la ubicación actual del dron y una coordenada objetivo utilizando la fórmula de Haversine.
* **Entradas:** Coordenada objetivo `destino` como `(latitud, longitud)` (tuple[float, float]).
* **Resultado:** Número flotante (`float`) representando la distancia estimada en kilómetros ($km$).

---

### **RF-04: Consultar Formato de Consola e Inspección Técnica**
* **Nombre:** Consultar Formato de Consola e Inspección Técnica
* **Resumen:** **Actor:** Operador de Monitoreo / Desarrollador. Proporciona representaciones formateadas legibles para la consola de operaciones (`__str__`) o representaciones técnicas precisas para depuración (`__repr__`).
* **Entradas:** Ninguna (invocado sobre la instancia).
* **Resultado:** Cadena de texto formateada con los datos consolidados del dron.
